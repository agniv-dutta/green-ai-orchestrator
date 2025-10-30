from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
import uuid

from database import get_db, MLJob
from predict import predict_carbon, find_greenest_region, REGION_CARBON

app = FastAPI(
    title="GreenML Optimizer API",
    description="Carbon prediction and optimization for ML workloads",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class JobRequest(BaseModel):
    model_type: str  # ResNet50, BERT-Base, GPT-2, ViT, YOLO, CNN-Small
    batch_size: int
    dataset_size_gb: int
    gpu_count: int
    gpu_type: str  # T4, V100, A100
    duration_hours: float
    region: str

class JobResponse(BaseModel):
    job_id: str
    predicted_carbon_kg: float
    region: str
    greenest_region: str
    potential_savings_kg: float
    savings_percentage: float
    carbon_by_region: dict
    timestamp: datetime

class StatsResponse(BaseModel):
    total_jobs: int
    total_carbon_predicted_kg: float
    total_potential_savings_kg: float
    average_savings_percentage: float
    jobs_by_region: dict
    jobs_by_model: dict

# Routes
@app.get("/")
def root():
    return {
        "message": "GreenML Optimizer API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "predict": "/predict",
            "jobs": "/jobs",
            "stats": "/stats",
            "regions": "/regions"
        }
    }

@app.get("/regions")
def get_regions():
    """Get available regions and their carbon intensity"""
    return {
        "regions": [
            {"name": region, "carbon_intensity": intensity, "unit": "kg CO2/kWh"}
            for region, intensity in REGION_CARBON.items()
        ]
    }

@app.post("/predict", response_model=JobResponse)
def predict_job(job: JobRequest, db: Session = Depends(get_db)):
    """
    Predict carbon emissions for an ML job and find optimization opportunities
    """
    # Validate inputs
    valid_models = ['ResNet50', 'BERT-Base', 'GPT-2', 'ViT', 'YOLO', 'CNN-Small']
    valid_gpus = ['T4', 'V100', 'A100']
    valid_regions = list(REGION_CARBON.keys())
    
    if job.model_type not in valid_models:
        raise HTTPException(status_code=400, detail=f"Invalid model_type. Must be one of: {valid_models}")
    if job.gpu_type not in valid_gpus:
        raise HTTPException(status_code=400, detail=f"Invalid gpu_type. Must be one of: {valid_gpus}")
    if job.region not in valid_regions:
        raise HTTPException(status_code=400, detail=f"Invalid region. Must be one of: {valid_regions}")
    
    # Predict carbon for requested configuration
    predicted_carbon = predict_carbon(
        model_type=job.model_type,
        batch_size=job.batch_size,
        dataset_size_gb=job.dataset_size_gb,
        gpu_count=job.gpu_count,
        gpu_type=job.gpu_type,
        duration_hours=job.duration_hours,
        region=job.region
    )
    
    # Find greenest region
    greenest_region, carbon_by_region = find_greenest_region(
        model_type=job.model_type,
        batch_size=job.batch_size,
        dataset_size_gb=job.dataset_size_gb,
        gpu_count=job.gpu_count,
        gpu_type=job.gpu_type,
        duration_hours=job.duration_hours
    )
    
    # Calculate savings
    greenest_carbon = carbon_by_region[greenest_region]
    potential_savings = predicted_carbon - greenest_carbon
    savings_percentage = (potential_savings / predicted_carbon * 100) if predicted_carbon > 0 else 0
    
    # Save to database
    job_id = f"job-{uuid.uuid4().hex[:8]}"
    db_job = MLJob(
        job_id=job_id,
        model_type=job.model_type,
        batch_size=job.batch_size,
        dataset_size_gb=job.dataset_size_gb,
        gpu_count=job.gpu_count,
        gpu_type=job.gpu_type,
        duration_hours=job.duration_hours,
        region=job.region,
        predicted_carbon_kg=predicted_carbon,
        greenest_region=greenest_region,
        potential_savings_kg=potential_savings
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    return JobResponse(
        job_id=job_id,
        predicted_carbon_kg=round(predicted_carbon, 3),
        region=job.region,
        greenest_region=greenest_region,
        potential_savings_kg=round(potential_savings, 3),
        savings_percentage=round(savings_percentage, 2),
        carbon_by_region={k: round(v, 3) for k, v in carbon_by_region.items()},
        timestamp=db_job.created_at
    )

@app.get("/jobs", response_model=List[JobResponse])
def list_jobs(limit: int = 100, db: Session = Depends(get_db)):
    """Get all jobs"""
    jobs = db.query(MLJob).order_by(MLJob.created_at.desc()).limit(limit).all()
    
    return [
        JobResponse(
            job_id=job.job_id,
            predicted_carbon_kg=job.predicted_carbon_kg,
            region=job.region,
            greenest_region=job.greenest_region,
            potential_savings_kg=job.potential_savings_kg,
            savings_percentage=(job.potential_savings_kg / job.predicted_carbon_kg * 100) if job.predicted_carbon_kg > 0 else 0,
            carbon_by_region={},  # Not stored individually
            timestamp=job.created_at
        )
        for job in jobs
    ]

@app.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """Get overall statistics"""
    total_jobs = db.query(func.count(MLJob.id)).scalar()
    total_carbon = db.query(func.sum(MLJob.predicted_carbon_kg)).scalar() or 0
    total_savings = db.query(func.sum(MLJob.potential_savings_kg)).scalar() or 0
    
    avg_savings_pct = (total_savings / total_carbon * 100) if total_carbon > 0 else 0
    
    # Jobs by region
    jobs_by_region = {}
    region_counts = db.query(MLJob.region, func.count(MLJob.id)).group_by(MLJob.region).all()
    for region, count in region_counts:
        jobs_by_region[region] = count
    
    # Jobs by model
    jobs_by_model = {}
    model_counts = db.query(MLJob.model_type, func.count(MLJob.id)).group_by(MLJob.model_type).all()
    for model, count in model_counts:
        jobs_by_model[model] = count
    
    return StatsResponse(
        total_jobs=total_jobs,
        total_carbon_predicted_kg=round(total_carbon, 2),
        total_potential_savings_kg=round(total_savings, 2),
        average_savings_percentage=round(avg_savings_pct, 2),
        jobs_by_region=jobs_by_region,
        jobs_by_model=jobs_by_model
    )

@app.get("/health")
def health():
    return {"status": "healthy", "service": "GreenML Optimizer API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)