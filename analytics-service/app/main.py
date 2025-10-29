from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

from app.analytics.carbon_calculator import carbon_calculator
from app.analytics.esg_reporter import esg_reporter
from app.demo_data import generate_demo_workloads, get_demo_stats, generate_historical_trends
app = FastAPI(
    title="GreenAI Analytics Service",
    description="AI-powered carbon analytics and ESG reporting for cloud workloads",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
) 

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "GreenAI Analytics Service 🚀",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "analytics",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

# Carbon analysis endpoints
@app.post("/analyze-carbon")
async def analyze_carbon(workload_data: dict):
    """Analyze carbon savings for a single workload"""
    result = carbon_calculator.calculate_carbon_savings(workload_data)
    
    if result.get('status') == 'error':
        raise HTTPException(status_code=400, detail=result.get('error', 'Analysis failed'))
    
    return result

@app.post("/analyze-cost")
async def analyze_cost(workload_data: dict):
    """Analyze cost savings for a single workload"""
    result = carbon_calculator.calculate_cost_savings(workload_data)
    
    if result.get('status') == 'error':
        raise HTTPException(status_code=400, detail=result.get('error', 'Analysis failed'))
    
    return result

@app.post("/analyze-comprehensive")
async def analyze_comprehensive(workload_data: dict):
    """Comprehensive analysis with carbon + cost + optimization insights"""
    result = carbon_calculator.analyze_comprehensive(workload_data)
    
    if result.get('status') == 'error':
        raise HTTPException(status_code=400, detail=result.get('error', 'Comprehensive analysis failed'))
    
    return result

@app.post("/compare-regions")
async def compare_regions(workload_data: dict):
    """Compare carbon and cost across all available regions"""
    result = carbon_calculator.get_region_comparison(workload_data)
    
    if result.get('status') == 'error':
        raise HTTPException(status_code=400, detail=result.get('error', 'Region comparison failed'))
    
    return result

# ESG reporting endpoints
@app.post("/generate-esg-report")
async def generate_esg_report(workloads_data: list):
    """Generate comprehensive ESG compliance report for multiple workloads"""
    if not workloads_data:
        raise HTTPException(status_code=400, detail="No workload data provided")
    
    report = esg_reporter.generate_esg_report(workloads_data)
    return report

# Demo and sample data endpoints
@app.get("/demo-data")
async def get_demo_data():
    """Get comprehensive demo data for frontend development"""
    workloads = generate_demo_workloads(8)
    
    # Analyze each workload
    analyzed_workloads = []
    for workload in workloads:
        analysis = carbon_calculator.analyze_comprehensive(workload)
        analyzed_workloads.append({
            'workload': workload,
            'analysis': analysis
        })
    
    # Generate ESG report for all demo workloads
    carbon_data = [analysis['carbon_analysis'] for analysis in analyzed_workloads if analysis['analysis']['status'] == 'success']
    esg_report = esg_reporter.generate_esg_report(carbon_data)
    
    return {
        'workloads': analyzed_workloads,
        'stats': get_demo_stats(),
        'esg_report': esg_report,
        'historical_trends': generate_historical_trends(14),  # Last 14 days
        'summary': {
            'total_workloads': len(workloads),
            'successful_analyses': len([w for w in analyzed_workloads if w['analysis']['status'] == 'success']),
            'timestamp': datetime.now().isoformat()
        }
    }

@app.get("/demo-stats")
async def get_demo_stats_endpoint():
    """Get demo statistics for dashboard"""
    return get_demo_stats()

@app.get("/historical-trends")
async def get_historical_trends(days: int = 30):
    """Get historical trend data for charts"""
    if days > 365:
        raise HTTPException(status_code=400, detail="Maximum 365 days of historical data")
    
    return generate_historical_trends(days)

# Insights and recommendations
@app.get("/optimization-tips")
async def get_optimization_tips():
    """Get AI-powered optimization tips"""
    return {
        "tips": [
            {
                "tip": "Schedule batch workloads between 1 AM - 5 AM local time",
                "impact": "Reduces carbon by 15-25%",
                "effort": "LOW",
                "savings": "High carbon savings with minimal operational impact"
            },
            {
                "tip": "Use us-west-2 (Oregon) or eu-west-1 (Ireland) for lowest carbon intensity",
                "impact": "Reduces carbon by 20-40% compared to high-carbon regions",
                "effort": "MEDIUM", 
                "savings": "Significant environmental impact with moderate configuration changes"
            },
            {
                "tip": "Right-size over-provisioned instances (40% are typically over-provisioned)",
                "impact": "Reduces cost by 25-35% and carbon by 20-30%",
                "effort": "MEDIUM",
                "savings": "Direct cost savings with immediate environmental benefits"
            },
            {
                "tip": "Implement auto-scaling to match actual demand patterns",
                "impact": "Reduces waste by 50-70% during low-usage periods",
                "effort": "HIGH",
                "savings": "Optimal resource utilization with maximum efficiency"
            },
            {
                "tip": "Use spot instances for fault-tolerant batch processing",
                "impact": "Reduces cost by 60-90% with similar carbon footprint",
                "effort": "MEDIUM",
                "savings": "Massive cost reduction with maintained environmental efficiency"
            }
        ],
        "summary": {
            "potential_savings": "35-60% reduction in carbon footprint",
            "potential_cost_reduction": "40-70% reduction in cloud costs", 
            "implementation_timeline": "2-4 weeks for full optimization",
            "roi_timeline": "1-3 months"
        }
    }

@app.get("/region-insights")
async def get_region_insights():
    """Get insights about different cloud regions"""
    regions = {
        'us-west-2': {
            'name': 'Oregon, USA',
            'carbon_intensity': 350,
            'renewable_energy': '100%',
            'cost_index': 'Medium',
            'recommendation': 'Best overall for carbon efficiency'
        },
        'eu-west-1': {
            'name': 'Ireland', 
            'carbon_intensity': 280,
            'renewable_energy': '100%',
            'cost_index': 'High',
            'recommendation': 'Best for European compliance'
        },
        'us-east-1': {
            'name': 'N. Virginia, USA',
            'carbon_intensity': 380, 
            'renewable_energy': '50%',
            'cost_index': 'Low',
            'recommendation': 'Cost-effective but higher carbon'
        },
        'ap-south-1': {
            'name': 'Mumbai, India',
            'carbon_intensity': 720,
            'renewable_energy': '25%',
            'cost_index': 'Very Low', 
            'recommendation': 'Avoid for carbon-sensitive workloads'
        }
    }
    
    return {
        'regions': regions,
        'key_insights': [
            'eu-west-1 has the lowest carbon intensity among major regions',
            'ap-south-1 has 2x higher carbon intensity than us-west-2',
            'Cost savings in high-carbon regions may not justify environmental impact',
            'Consider time-of-day scheduling in addition to region selection'
        ]
    }

# Batch processing endpoints
@app.post("/analyze-batch")
async def analyze_batch_workloads(workloads_data: list):
    """Analyze multiple workloads in batch"""
    if not workloads_data:
        raise HTTPException(status_code=400, detail="No workloads provided")
    
    results = []
    for workload in workloads_data:
        analysis = carbon_calculator.analyze_comprehensive(workload)
        results.append(analysis)
    
    # Generate summary
    successful_analyses = [r for r in results if r.get('status') == 'success']
    
    if successful_analyses:
        total_carbon_saved = sum(item['total_savings']['carbon_kg'] for item in successful_analyses)
        total_cost_saved = sum(item['total_savings']['cost_usd'] for item in successful_analyses)
        
        summary = {
            'total_workloads_analyzed': len(workloads_data),
            'successful_analyses': len(successful_analyses),
            'total_carbon_savings_kg': round(total_carbon_saved, 2),
            'total_cost_savings_usd': round(total_cost_saved, 2),
            'average_savings_per_workload': {
                'carbon_kg': round(total_carbon_saved / len(successful_analyses), 2),
                'cost_usd': round(total_cost_saved / len(successful_analyses), 2)
            }
        }
    else:
        summary = {
            'total_workloads_analyzed': len(workloads_data),
            'successful_analyses': 0,
            'error': 'No successful analyses'
        }
    
    return {
        'results': results,
        'summary': summary,
        'timestamp': datetime.now().isoformat()
    }

# System information
@app.get("/system-info")
async def get_system_info():
    """Get information about the analytics service"""
    return {
        "service": "GreenAI Analytics",
        "version": "2.0.0",
        "status": "operational",
        "endpoints_available": [
            "/analyze-carbon", "/analyze-cost", "/analyze-comprehensive",
            "/generate-esg-report", "/demo-data", "/optimization-tips",
            "/compare-regions", "/analyze-batch"
        ],
        "features": [
            "Real-time carbon calculations",
            "Cost savings analysis", 
            "ESG compliance reporting",
            "Region comparison engine",
            "AI-powered recommendations",
            "Historical trend analysis",
            "Batch processing support"
        ],
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)