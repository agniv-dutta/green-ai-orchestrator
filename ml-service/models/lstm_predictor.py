import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import MinMaxScaler
import joblib
from loguru import logger
from typing import Dict, List, Tuple
import json
#from app.utils.logger import logger

class LSTMModel(nn.Module):
    """PyTorch LSTM Model"""
    
    def __init__(self, input_size: int, hidden_size: int, num_layers: int, output_size: int, dropout: float = 0.2):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        self.fc1 = nn.Linear(hidden_size, 50)
        self.fc2 = nn.Linear(50, output_size)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        # Initialize hidden state
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        
        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0, c0))
        
        # Take the last output
        out = out[:, -1, :]
        
        # Fully connected layers
        out = self.relu(self.fc1(out))
        out = self.dropout(out)
        out = self.fc2(out)
        
        return out


class LSTMPredictor:
    """LSTM model for resource usage and carbon intensity forecasting using PyTorch"""
    
    def __init__(self, sequence_length: int = 24, forecast_horizon: int = 12):
        self.sequence_length = sequence_length
        self.forecast_horizon = forecast_horizon
        self.model = None
        self.scalers = {}
        self.is_trained = False
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    def build_model(self, input_size: int) -> LSTMModel:
        """Build PyTorch LSTM model"""
        model = LSTMModel(
            input_size=input_size,
            hidden_size=100,
            num_layers=2,
            output_size=self.forecast_horizon * input_size,  # Predict all features for horizon
            dropout=0.2
        )
        return model.to(self.device)
    
    def prepare_data(self, data: pd.DataFrame, target_columns: List[str]) -> Tuple[torch.Tensor, torch.Tensor]:
        """Prepare data for LSTM training"""
        sequences = []
        targets = []
        
        for col in target_columns:
            if col not in self.scalers:
                self.scalers[col] = MinMaxScaler()
                data[col] = self.scalers[col].fit_transform(data[[col]])
        
        for i in range(len(data) - self.sequence_length - self.forecast_horizon + 1):
            seq = data[target_columns].iloc[i:i + self.sequence_length].values
            target = data[target_columns].iloc[i + self.sequence_length:i + self.sequence_length + self.forecast_horizon].values.flatten()
            sequences.append(seq)
            targets.append(target)
        
        return torch.FloatTensor(np.array(sequences)), torch.FloatTensor(np.array(targets))
    
    def train(self, historical_data: pd.DataFrame, target_columns: List[str], epochs: int = 100) -> Dict:
        """Train the LSTM model"""
        logger.info(f"Training LSTM model on {len(historical_data)} samples using {self.device}")
        
        # Prepare data
        X, y = self.prepare_data(historical_data, target_columns)
        X, y = X.to(self.device), y.to(self.device)
        
        # Build model
        self.model = self.build_model(len(target_columns))
        
        # Loss and optimizer
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        
        # Training loop
        train_losses = []
        for epoch in range(epochs):
            self.model.train()
            
            # Forward pass
            outputs = self.model(X)
            loss = criterion(outputs, y)
            
            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            train_losses.append(loss.item())
            
            if epoch % 20 == 0:
                logger.info(f'Epoch [{epoch}/{epochs}], Loss: {loss.item():.6f}')
        
        self.is_trained = True
        logger.info("LSTM model training completed")
        
        return {
            'final_loss': train_losses[-1],
            'min_loss': min(train_losses),
            'training_samples': len(X)
        }
    
    def predict(self, recent_data: pd.DataFrame, target_columns: List[str]) -> Dict[str, List[float]]:
        """Make predictions using trained model"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        self.model.eval()
        
        # Prepare input data
        for col in target_columns:
            if col in self.scalers:
                recent_data[col] = self.scalers[col].transform(recent_data[[col]])
        
        # Ensure we have enough data for sequence
        if len(recent_data) < self.sequence_length:
            raise ValueError(f"Need at least {self.sequence_length} data points for prediction")
        
        # Take the most recent sequence
        input_seq = recent_data[target_columns].iloc[-self.sequence_length:].values
        input_tensor = torch.FloatTensor(input_seq).unsqueeze(0).to(self.device)
        
        # Make prediction
        with torch.no_grad():
            prediction = self.model(input_tensor).cpu().numpy()[0]
        
        # Reshape and inverse transform
        prediction_reshaped = prediction.reshape(self.forecast_horizon, len(target_columns))
        
        results = {}
        for i, col in enumerate(target_columns):
            if col in self.scalers:
                col_predictions = prediction_reshaped[:, i].reshape(-1, 1)
                results[col] = self.scalers[col].inverse_transform(col_predictions).flatten().tolist()
        
        return results
    
    def save_model(self, filepath: str):
        """Save model and scalers"""
        if self.model:
            torch.save({
                'model_state_dict': self.model.state_dict(),
                'model_config': {
                    'input_size': len(next(iter(self.scalers.keys()))) if self.scalers else 1,
                    'hidden_size': 100,
                    'num_layers': 2,
                    'output_size': self.forecast_horizon
                }
            }, f"{filepath}_model.pth")
        joblib.dump(self.scalers, f"{filepath}_scalers.pkl")
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load model and scalers"""
        checkpoint = torch.load(f"{filepath}_model.pth", map_location=self.device)
        self.scalers = joblib.load(f"{filepath}_scalers.pkl")
        
        # Rebuild model
        config = checkpoint['model_config']
        self.model = LSTMModel(
            input_size=config['input_size'],
            hidden_size=config['hidden_size'],
            num_layers=config['num_layers'],
            output_size=config['output_size']
        ).to(self.device)
        
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.is_trained = True
        logger.info(f"Model loaded from {filepath}")