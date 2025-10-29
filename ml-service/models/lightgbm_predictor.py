import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.preprocessing import MinMaxScaler
import joblib
from loguru import logger
from typing import Dict, List


class LightGBMPredictor:
    """LightGBM model for time series forecasting (simpler alternative)"""
    
    def __init__(self, forecast_horizon: int = 12):
        self.forecast_horizon = forecast_horizon
        self.models = {}
        self.scalers = {}
        self.is_trained = False
    
    def create_features(self, data: pd.DataFrame, target_columns: List[str]) -> pd.DataFrame:
        """Create time series features"""
        df = data.copy()
        
        # Lag features
        for lag in [1, 2, 3, 6, 12, 24]:
            for col in target_columns:
                df[f'{col}_lag_{lag}'] = df[col].shift(lag)
        
        # Rolling statistics
        for window in [3, 6, 12]:
            for col in target_columns:
                df[f'{col}_roll_mean_{window}'] = df[col].rolling(window).mean()
                df[f'{col}_roll_std_{window}'] = df[col].rolling(window).std()
        
        # Time features
        if 'timestamp' in df.columns:
            df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
            df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
            df['month'] = pd.to_datetime(df['timestamp']).dt.month
        
        return df.dropna()
    
    def train(self, historical_data: pd.DataFrame, target_columns: List[str]) -> Dict:
        """Train LightGBM models"""
        logger.info("Training LightGBM models")
        
        # Create features
        feature_data = self.create_features(historical_data, target_columns)
        
        for col in target_columns:
            # Scale target
            self.scalers[col] = MinMaxScaler()
            y = self.scalers[col].fit_transform(feature_data[[col]])
            
            # Prepare features (exclude target columns for this specific target)
            feature_cols = [c for c in feature_data.columns if c not in target_columns]
            X = feature_data[feature_cols]
            
            # Train model
            model = lgb.LGBMRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            )
            
            model.fit(X, y.ravel())
            self.models[col] = model
            
            logger.info(f"Trained model for {col}")
        
        self.is_trained = True
        return {'status': 'success', 'models_trained': len(target_columns)}
    
    def predict(self, recent_data: pd.DataFrame, target_columns: List[str]) -> Dict[str, List[float]]:
        """Make predictions using trained model"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Create features for prediction
        feature_data = self.create_features(recent_data, target_columns)
        
        results = {}
        for col in target_columns:
            if col in self.models:
                # Prepare features for this target
                feature_cols = [c for c in feature_data.columns if c not in target_columns]
                X_pred = feature_data[feature_cols].iloc[-1:].values
                
                # Make prediction
                prediction_scaled = self.models[col].predict(X_pred)[0]
                
                # Inverse transform
                prediction = self.scalers[col].inverse_transform([[prediction_scaled]])[0][0]
                results[col] = [prediction] * self.forecast_horizon  # Repeat for horizon
        
        return results
    
    def save_model(self, filepath: str):
        """Save models and scalers"""
        model_data = {
            'models': self.models,
            'scalers': self.scalers
        }
        joblib.dump(model_data, filepath)
        logger.info(f"LightGBM models saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load models and scalers"""
        model_data = joblib.load(filepath)
        self.models = model_data['models']
        self.scalers = model_data['scalers']
        self.is_trained = True
        logger.info(f"LightGBM models loaded from {filepath}")