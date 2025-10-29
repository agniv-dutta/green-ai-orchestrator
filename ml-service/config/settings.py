from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    DEBUG: bool = True
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8001
    
    # WattTime API
    WATTTIME_API_KEY: Optional[str] = None
    WATTTIME_USERNAME: Optional[str] = None
    WATTTIME_PASSWORD: Optional[str] = None
    
    # Model paths
    LSTM_MODEL_PATH: str = "models/saved/lstm_model"
    RL_MODEL_PATH: str = "models/saved/rl_model"
    PROFILER_MODEL_PATH: str = "models/saved/profiler_model.pkl"
    
    # Carbon data
    DEFAULT_LATITUDE: float = 37.7749  # San Francisco
    DEFAULT_LONGITUDE: float = -122.4194
    
    class Config:
        env_file = ".env"

settings = Settings()