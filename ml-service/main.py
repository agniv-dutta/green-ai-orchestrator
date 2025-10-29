from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys

# Add the current directory to Python path to fix imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your modules
try:
    from api.endpoints import router as api_router
    from config.settings import settings
    from utils.logger import setup_logging
    from models.lstm_predictor import LSTMPredictor
    from models.rl_scheduler import RLWorkloadScheduler
    from models.workload_profiler import WorkloadProfiler
    print("All imports successful!")
except ImportError as e:
    print(f"Import error: {e}")
    print("Please check your directory structure and __init__.py files")

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="GreenAI ML Service",
    description="Machine Learning service for carbon-aware AI workload scheduling",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML models (singleton instances)
lstm_predictor = None
rl_scheduler = None
workload_profiler = None

@app.on_event("startup")
async def startup_event():
    """Initialize ML models when the application starts"""
    global lstm_predictor, rl_scheduler, workload_profiler
    
    try:
        from models.lstm_predictor import LSTMPredictor
        from models.rl_scheduler import RLWorkloadScheduler
        from models.workload_profiler import WorkloadProfiler
        
        lstm_predictor = LSTMPredictor()
        rl_scheduler = RLWorkloadScheduler()
        workload_profiler = WorkloadProfiler()
        
        print("GreenAI ML Models Initialized:")
        print("   - LSTM Predictor: Ready for carbon forecasting")
        print("   - RL Scheduler: Ready for workload optimization") 
        print("   - Workload Profiler: Ready for resource prediction")
        
    except Exception as e:
        print(f"Model initialization failed: {e}")

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "message": "GreenAI ML Service is running",
        "status": "healthy",
        "service": "Carbon-aware AI Workload Scheduling",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "api_base": "/api/v1"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    models_status = {
        "lstm_predictor": lstm_predictor is not None,
        "rl_scheduler": rl_scheduler is not None,
        "workload_profiler": workload_profiler is not None
    }
    
    all_healthy = all(models_status.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "service": "ml-service",
        "models_initialized": models_status,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }

# Demo endpoint for quick testing
@app.get("/demo")
async def demo():
    """Demo endpoint to test basic functionality"""
    try:
        # Sample carbon forecast (simulated)
        carbon_forecast = [0.8, 0.6, 0.3, 0.2, 0.1, 0.4, 0.7, 0.9] * 3
        
        # Sample workloads
        sample_workloads = [
            {
                "id": 1,
                "compute_requirements": 0.5,
                "duration": 2,
                "deadline": 6,
                "priority": 1,
                "workload_type": "inference"
            },
            {
                "id": 2, 
                "compute_requirements": 0.8,
                "duration": 1,
                "deadline": 12,
                "priority": 2,
                "workload_type": "training"
            }
        ]
        
        # Test scheduling
        if rl_scheduler:
            schedule = rl_scheduler.schedule_workloads(sample_workloads, carbon_forecast)
        else:
            schedule = []
        
        return {
            "status": "success",
            "message": "GreenAI ML Service Demo",
            "carbon_forecast_sample": carbon_forecast[:8],  # First 8 hours
            "sample_workloads": sample_workloads,
            "schedule_preview": schedule[:2] if schedule else [],
            "models_ready": lstm_predictor is not None and rl_scheduler is not None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo error: {str(e)}")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "endpoint": str(request.url)
        }
    )

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )