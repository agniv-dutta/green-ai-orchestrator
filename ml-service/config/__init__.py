"""
Configuration package for GreenAI ML Service

Contains settings and configuration management for:
- API settings
- Model paths
- External service credentials (WattTime API)
- Environment variables
"""

from .settings import settings

__all__ = ["settings"]

__version__ = "1.0.0"