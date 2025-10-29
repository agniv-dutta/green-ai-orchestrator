"""
GreenAI ML Service API Package

This package contains all API endpoints for the ML service including:
- Carbon intensity prediction and forecasting
- Workload scheduling optimization  
- Workload profiling and resource prediction
- Model training endpoints
"""

from .endpoints import router

__all__ = ["router"]

__version__ = "1.0.0"
__author__ = "GreenAI Team"
__description__ = "ML Service API for carbon-aware AI workload scheduling"