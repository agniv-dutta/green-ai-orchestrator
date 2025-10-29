import pandas as pd
import numpy as np
from typing import Dict, List, Any
from loguru import logger


class DataProcessor:
    """Data processing utilities for ML service"""
    
    @staticmethod
    def create_time_features(df: pd.DataFrame, timestamp_col: str = 'timestamp') -> pd.DataFrame:
        """Create time-based features from timestamp"""
        df_processed = df.copy()
        
        if timestamp_col in df_processed.columns:
            df_processed[timestamp_col] = pd.to_datetime(df_processed[timestamp_col])
            df_processed['hour'] = df_processed[timestamp_col].dt.hour
            df_processed['day_of_week'] = df_processed[timestamp_col].dt.dayofweek
            df_processed['month'] = df_processed[timestamp_col].dt.month
            df_processed['is_weekend'] = df_processed['day_of_week'].isin([5, 6]).astype(int)
        
        return df_processed
    
    @staticmethod
    def normalize_data(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Normalize specified columns to 0-1 range"""
        df_normalized = df.copy()
        
        for col in columns:
            if col in df_normalized.columns:
                min_val = df_normalized[col].min()
                max_val = df_normalized[col].max()
                if max_val > min_val:
                    df_normalized[col] = (df_normalized[col] - min_val) / (max_val - min_val)
        
        return df_normalized
    
    @staticmethod
    def generate_sample_workloads(count: int = 10) -> List[Dict]:
        """Generate sample workloads for testing"""
        workloads = []
        
        for i in range(count):
            workloads.append({
                'id': i,
                'compute_requirements': np.random.uniform(0.1, 1.0),
                'duration': np.random.randint(1, 6),
                'deadline': np.random.randint(4, 24),
                'priority': np.random.choice([1, 2, 3], p=[0.2, 0.5, 0.3]),
                'workload_type': np.random.choice(['inference', 'training', 'finetuning'])
            })
        
        return workloads