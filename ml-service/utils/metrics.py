import numpy as np
from typing import Dict, List, Any
from loguru import logger

class MetricsCalculator:
    """Calculate performance metrics for ML models"""
    
    @staticmethod
    def calculate_accuracy(predictions: List[float], actuals: List[float]) -> Dict[str, float]:
        """Calculate prediction accuracy metrics"""
        if len(predictions) != len(actuals):
            raise ValueError("Predictions and actuals must have same length")
        
        predictions = np.array(predictions)
        actuals = np.array(actuals)
        
        # Calculate various metrics
        mae = np.mean(np.abs(predictions - actuals))
        mse = np.mean((predictions - actuals) ** 2)
        rmse = np.sqrt(mse)
        
        # Calculate mean absolute percentage error (avoid division by zero)
        non_zero_mask = actuals != 0
        if np.any(non_zero_mask):
            mape = np.mean(np.abs((predictions[non_zero_mask] - actuals[non_zero_mask]) / actuals[non_zero_mask])) * 100
        else:
            mape = 0
        
        return {
            'mae': float(mae),
            'mse': float(mse),
            'rmse': float(rmse),
            'mape': float(mape),
            'samples': len(predictions)
        }
    
    @staticmethod
    def calculate_carbon_savings(baseline: List[float], optimized: List[float]) -> Dict[str, float]:
        """Calculate carbon savings metrics"""
        baseline_total = sum(baseline)
        optimized_total = sum(optimized)
        
        if baseline_total == 0:
            return {'savings_percent': 0, 'savings_absolute': 0}
        
        savings_absolute = baseline_total - optimized_total
        savings_percent = (savings_absolute / baseline_total) * 100
        
        return {
            'savings_percent': float(savings_percent),
            'savings_absolute': float(savings_absolute),
            'baseline_total': float(baseline_total),
            'optimized_total': float(optimized_total)
        }