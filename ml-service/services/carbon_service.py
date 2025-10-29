import requests
import pandas as pd
from typing import Dict, List, Optional
from loguru import logger
import time
import os
import numpy as np


class CarbonIntensityService:
    """Service for fetching and managing carbon intensity data"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('WATTTIME_API_KEY')
        self.base_url = "https://api.watttime.org/v2"
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def get_current_carbon_intensity(self, latitude: float, longitude: float) -> Optional[float]:
        """Get current carbon intensity for a location"""
        try:
            logger.info(f"Fetching carbon data for lat={latitude}, lon={longitude}")
            
            # For demo purposes, return simulated data
            # In production, you would use the actual API
            return self.simulate_carbon_data().iloc[0]['carbon_intensity']
            
        except Exception as e:
            logger.error(f"Error fetching carbon intensity: {e}")
            return None
    
    def get_forecast(self, latitude: float, longitude: float, 
                    hours: int = 24) -> Optional[pd.DataFrame]:
        """Get carbon intensity forecast"""
        try:
            logger.info(f"Fetching {hours}h forecast for lat={latitude}, lon={longitude}")
            
            # Return simulated forecast
            return self.simulate_carbon_data(hours=hours)
            
        except Exception as e:
            logger.error(f"Error fetching carbon forecast: {e}")
            return None
    
    def simulate_carbon_data(self, hours: int = 24, pattern: str = "daily") -> pd.DataFrame:
        """Simulate carbon data for testing"""
        logger.info(f"Generating simulated carbon data for {hours} hours")
        
        if pattern == "daily":
            # Simulate daily pattern with lower carbon at night
            base_pattern = [0.3, 0.2, 0.1, 0.1, 0.1, 0.2,  # Night (low)
                          0.4, 0.6, 0.7, 0.8, 0.8, 0.7,  # Morning (medium)
                          0.8, 0.9, 0.9, 0.8, 0.7, 0.6,  # Afternoon (high)
                          0.5, 0.4, 0.3, 0.3, 0.2, 0.2]  # Evening (medium-low)
        
        # Repeat or truncate pattern to match hours
        if hours <= 24:
            carbon_data = base_pattern[:hours]
        else:
            carbon_data = (base_pattern * (hours // 24 + 1))[:hours]
        
        # Add some randomness
        carbon_data = [max(0.05, min(0.95, x + np.random.normal(0, 0.05))) for x in carbon_data]
        
        # Create DataFrame with timestamps
        timestamps = pd.date_range(start=pd.Timestamp.now(), periods=hours, freq='H')
        
        return pd.DataFrame({
            'timestamp': timestamps,
            'carbon_intensity': carbon_data,
            'source': 'simulated'
        })