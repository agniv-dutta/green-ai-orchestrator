from fastapi import APIRouter, HTTPException
from loguru import logger
from typing import Dict, List, Any
import pandas as pd

from models.lstm_predictor import LSTMPredictor
from models.rl_scheduler import RLWorkloadScheduler
from models.workload_profiler import WorkloadProfiler
from services.carbon_service import CarbonIntensityService
from services.optimization_engine import GreenAIOptimizationEngine

router = APIRouter()

# Initialize models
lstm_predictor = LSTMPredictor()
rl_scheduler = RLWorkloadScheduler()
workload_profiler = WorkloadProfiler()
carbon_service = CarbonIntensityService()
optimization_engine = GreenAIOptimizationEngine()

@router.get("/")
async def root():
    return {"message": "GreenAI ML Service API", "status": "active"}

@router.post("/predict/carbon")
async def predict_carbon_intensity(historical_data: Dict[str, Any]):
    """Predict carbon intensity using LSTM"""
    try:
        df = pd.DataFrame(historical_data['data'])
        target_columns = historical_data.get('target_columns', ['carbon_intensity'])
        
        # For demo, we'll use simulated prediction
        # In production, you would train the model first
        prediction = lstm_predictor.predict(df, target_columns)
        
        return {
            "status": "success",
            "prediction": prediction,
            "model": "LSTM"
        }
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/schedule/workloads")
async def schedule_workloads(schedule_request: Dict[str, Any]):
    """Schedule workloads using carbon-aware optimization"""
    try:
        workloads = schedule_request['workloads']
        carbon_forecast = schedule_request['carbon_forecast']
        strategy = schedule_request.get('strategy', 'carbon_aware')
        
        # Use optimization engine
        schedule = optimization_engine.optimize_schedule(
            workloads, 
            pd.DataFrame({'carbon_intensity': carbon_forecast}),
            strategy
        )
        
        return {
            "status": "success",
            "schedule": schedule,
            "strategy": strategy,
            "total_carbon": schedule.get('total_carbon', 0)
        }
    except Exception as e:
        logger.error(f"Scheduling error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/profile/workload")
async def profile_workload(workload_data: Dict[str, Any]):
    """Profile workload and predict resource requirements"""
    try:
        profile = workload_profiler.predict_workload_type(workload_data)
        
        return {
            "status": "success",
            "workload_type": profile['workload_type'],
            "predicted_resources": {
                "cpu": profile['predicted_cpu'],
                "memory": profile['predicted_memory'],
                "gpu": profile['predicted_gpu'],
                "duration": profile['predicted_duration']
            },
            "cluster_id": profile['cluster_id']
        }
    except Exception as e:
        logger.error(f"Profiling error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/carbon/current")
async def get_current_carbon(latitude: float, longitude: float):
    """Get current carbon intensity for location"""
    try:
        carbon_intensity = carbon_service.get_current_carbon_intensity(latitude, longitude)
        
        if carbon_intensity is None:
            # Fallback to simulated data
            simulated_data = carbon_service.simulate_carbon_data()
            carbon_intensity = simulated_data['carbon_intensity'].iloc[0]
        
        return {
            "status": "success",
            "carbon_intensity": carbon_intensity,
            "latitude": latitude,
            "longitude": longitude,
            "source": "watttime" if carbon_intensity else "simulated"
        }
    except Exception as e:
        logger.error(f"Carbon data error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/carbon/forecast")
async def get_carbon_forecast(latitude: float, longitude: float, hours: int = 24):
    """Get carbon intensity forecast"""
    try:
        forecast = carbon_service.get_forecast(latitude, longitude, hours)
        
        if forecast is None:
            # Fallback to simulated data
            forecast = carbon_service.simulate_carbon_data()
        
        return {
            "status": "success",
            "forecast": forecast.to_dict('records'),
            "hours": hours,
            "source": "watttime" if forecast is not None else "simulated"
        }
    except Exception as e:
        logger.error(f"Carbon forecast error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train/lstm")
async def train_lstm_model(training_data: Dict[str, Any]):
    """Train the LSTM model"""
    try:
        df = pd.DataFrame(training_data['data'])
        target_columns = training_data.get('target_columns', ['carbon_intensity'])
        epochs = training_data.get('epochs', 100)
        
        results = lstm_predictor.train(df, target_columns, epochs)
        
        return {
            "status": "success",
            "training_results": results,
            "message": "LSTM model trained successfully"
        }
    except Exception as e:
        logger.error(f"Training error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ml-service",
        "models_ready": True
    }