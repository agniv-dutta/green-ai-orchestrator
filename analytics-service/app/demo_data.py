from datetime import datetime, timedelta
import random
from typing import List, Dict

def generate_demo_workloads(count: int = 10) -> List[Dict]:
    """Generate realistic demo workloads"""
    workload_types = ['ml_training', 'batch_processing', 'data_processing', 'inference', 'web_serving']
    regions = ['us-west-2', 'us-east-1', 'eu-west-1', 'ap-south-1', 'eu-central-1']
    
    workloads = []
    
    for i in range(count):
        workload_type = random.choice(workload_types)
        region = random.choice(regions)
        
        # Generate realistic resource specifications
        if workload_type == 'ml_training':
            resources = {'cpu': random.randint(8, 32), 'memory_gb': random.randint(32, 128), 'gpu': random.randint(1, 4)}
            duration = random.uniform(2.0, 8.0)
        elif workload_type == 'batch_processing':
            resources = {'cpu': random.randint(4, 16), 'memory_gb': random.randint(16, 64), 'gpu': 0}
            duration = random.uniform(1.0, 4.0)
        elif workload_type == 'data_processing':
            resources = {'cpu': random.randint(2, 8), 'memory_gb': random.randint(8, 32), 'gpu': 0}
            duration = random.uniform(0.5, 2.0)
        else:
            resources = {'cpu': random.randint(1, 4), 'memory_gb': random.randint(2, 16), 'gpu': 0}
            duration = random.uniform(0.1, 1.0)
        
        workload = {
            'workload_id': f"{workload_type}-{i+1}-{datetime.now().strftime('%H%M%S')}",
            'workload_type': workload_type,
            'region': region,
            'duration_hours': round(duration, 2),
            'resources': resources,
            'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 720))).isoformat(),
            'status': 'completed'
        }
        
        workloads.append(workload)
    
    return workloads

def get_demo_stats() -> Dict:
    """Get comprehensive demo statistics"""
    return {
        'summary': {
            'total_workloads_analyzed': 147,
            'time_period': 'Last 30 days',
            'report_generated': datetime.now().isoformat()
        },
        'carbon_impact': {
            'total_carbon_saved_kg': 2456.78,
            'total_carbon_saved_tons': 2.46,
            'equivalent_trees': 113,
            'equivalent_cars': 0.53,
            'percent_reduction': 42.3
        },
        'cost_impact': {
            'total_cost_saved_usd': 689.45,
            'estimated_annual_savings': 8273.40,
            'average_savings_per_workload': 4.69,
            'roi_percentage': 415
        },
        'performance_metrics': {
            'esg_score': 78.5,
            'compliance_status': 'ADVANCED',
            'optimization_efficiency': '87%',
            'preferred_region': 'eu-west-1'
        }
    }

def generate_historical_trends(days: int = 30) -> List[Dict]:
    """Generate historical trend data for charts"""
    trends = []
    base_date = datetime.now() - timedelta(days=days)
    
    cumulative_carbon = 0
    cumulative_cost = 0
    
    for day in range(days):
        date = base_date + timedelta(days=day)
        
        daily_carbon = random.uniform(50, 120)
        daily_cost = random.uniform(15, 35)
        
        cumulative_carbon += daily_carbon
        cumulative_cost += daily_cost
        
        trend_point = {
            'date': date.strftime('%Y-%m-%d'),
            'daily_carbon_saved_kg': round(daily_carbon, 2),
            'daily_cost_saved_usd': round(daily_cost, 2),
            'cumulative_carbon_kg': round(cumulative_carbon, 2),
            'cumulative_cost_usd': round(cumulative_cost, 2),
            'workloads_optimized': random.randint(3, 8)
        }
        
        trends.append(trend_point)
    
    return trends