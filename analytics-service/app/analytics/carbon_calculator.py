import pandas as pd
from datetime import datetime
from typing import Dict, List

class CarbonCalculator:
    def __init__(self):
        self.carbon_intensity_data = {
            'us-west-2': 350,  # gCO2/kWh - Oregon
            'us-east-1': 380,  # N. Virginia
            'eu-west-1': 280,  # Ireland
            'ap-south-1': 720, # Mumbai
            'eu-central-1': 320, # Frankfurt
            'ap-southeast-1': 650, # Singapore
            'default': 450
        }
        
        self.cost_data = {
            'us-west-2': 0.023,  # $ per hour for c5.xlarge equivalent
            'us-east-1': 0.025,
            'eu-west-1': 0.027,
            'ap-south-1': 0.018,
            'eu-central-1': 0.029,
            'ap-southeast-1': 0.026,
            'default': 0.025
        }
        
        self.optimization_factors = {
            'ml_training': 0.55,  # 45% savings
            'batch_processing': 0.60,  # 40% savings
            'data_processing': 0.65,  # 35% savings
            'inference': 0.70,  # 30% savings
            'web_serving': 0.75,  # 25% savings
            'default': 0.60  # 40% savings
        }
    
    def calculate_carbon_savings(self, workload_data: Dict) -> Dict:
        """Calculate carbon savings for a workload"""
        try:
            region = workload_data.get('region', 'default')
            duration_hours = workload_data.get('duration_hours', 1)
            resources = workload_data.get('resources', {})
            workload_type = workload_data.get('type', 'default')
            
            baseline_carbon = self._calculate_baseline_carbon(region, duration_hours, resources)
            optimized_carbon = self._calculate_optimized_carbon(region, duration_hours, resources, workload_type)
            savings = baseline_carbon - optimized_carbon
            
            return {
                'baseline_carbon_kg': round(baseline_carbon, 2),
                'optimized_carbon_kg': round(optimized_carbon, 2),
                'carbon_savings_kg': round(savings, 2),
                'savings_percentage': round((savings / baseline_carbon) * 100, 1),
                'region': region,
                'workload_type': workload_type,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
            
        except Exception as e:
            return {'error': str(e), 'status': 'error'}
    
    def calculate_cost_savings(self, workload_data: Dict) -> Dict:
        """Calculate cost savings from optimization"""
        try:
            region = workload_data.get('region', 'default')
            duration_hours = workload_data.get('duration_hours', 1)
            resources = workload_data.get('resources', {})
            workload_type = workload_data.get('type', 'default')
            
            baseline_cost = self._calculate_baseline_cost(region, duration_hours, resources)
            optimized_cost = self._calculate_optimized_cost(region, duration_hours, resources, workload_type)
            savings = baseline_cost - optimized_cost
            
            return {
                'baseline_cost_usd': round(baseline_cost, 2),
                'optimized_cost_usd': round(optimized_cost, 2),
                'cost_savings_usd': round(savings, 2),
                'cost_savings_percent': round((savings / baseline_cost) * 100, 1),
                'region': region,
                'workload_type': workload_type,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
            
        except Exception as e:
            return {'error': str(e), 'status': 'error'}
    
    def analyze_comprehensive(self, workload_data: Dict) -> Dict:
        """Comprehensive analysis with carbon + cost"""
        carbon_result = self.calculate_carbon_savings(workload_data)
        cost_result = self.calculate_cost_savings(workload_data)
        
        if carbon_result['status'] == 'success' and cost_result['status'] == 'success':
            return {
                'carbon_analysis': carbon_result,
                'cost_analysis': cost_result,
                'total_savings': {
                    'carbon_kg': carbon_result['carbon_savings_kg'],
                    'cost_usd': cost_result['cost_savings_usd'],
                    'savings_ratio': round(cost_result['cost_savings_usd'] / carbon_result['carbon_savings_kg'], 2)
                },
                'workload_id': workload_data.get('workload_id', 'unknown'),
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
        else:
            return {'error': 'Analysis failed', 'status': 'error'}
    
    def _calculate_baseline_carbon(self, region: str, duration: float, resources: Dict) -> float:
        """Calculate carbon for non-optimized workload"""
        carbon_intensity = self.carbon_intensity_data.get(region, self.carbon_intensity_data['default'])
        
        # Advanced model considering different resource types
        cpu = resources.get('cpu', 1)
        memory = resources.get('memory_gb', 2)
        gpu = resources.get('gpu', 0)
        storage = resources.get('storage_gb', 0)
        
        # Energy consumption model (kWh)
        energy_kwh = (
            (cpu * 0.08) +          # CPU power
            (memory * 0.03) +       # Memory power
            (gpu * 0.25) +          # GPU power (if any)
            (storage * 0.0005)      # Storage power (negligible)
        ) * duration
        
        carbon_g = energy_kwh * carbon_intensity
        return carbon_g / 1000  # Convert to kg
    
    def _calculate_optimized_carbon(self, region: str, duration: float, resources: Dict, workload_type: str) -> float:
        """Calculate carbon for GreenAI-optimized workload"""
        baseline = self._calculate_baseline_carbon(region, duration, resources)
        optimization_factor = self.optimization_factors.get(workload_type, self.optimization_factors['default'])
        optimized = baseline * optimization_factor
        
        return optimized
    
    def _calculate_baseline_cost(self, region: str, duration: float, resources: Dict) -> float:
        """Calculate cost for non-optimized workload"""
        hourly_rate = self.cost_data.get(region, self.cost_data['default'])
        
        cpu = resources.get('cpu', 1)
        memory = resources.get('memory_gb', 2)
        gpu = resources.get('gpu', 0)
        storage = resources.get('storage_gb', 0)
        
        # Cost model based on resource usage
        baseline_cost = (
            (cpu * 0.15) +          # CPU cost factor
            (memory * 0.08) +       # Memory cost factor
            (gpu * 1.50) +          # GPU cost factor
            (storage * 0.0001)      # Storage cost factor
        ) * hourly_rate * duration
        
        return baseline_cost
    
    def _calculate_optimized_cost(self, region: str, duration: float, resources: Dict, workload_type: str) -> float:
        """Calculate cost for GreenAI-optimized workload"""
        baseline = self._calculate_baseline_cost(region, duration, resources)
        optimization_factor = self.optimization_factors.get(workload_type, self.optimization_factors['default'])
        optimized = baseline * optimization_factor
        
        return optimized
    
    def get_region_comparison(self, workload_data: Dict) -> Dict:
        """Compare carbon and cost across all regions"""
        original_region = workload_data.get('region', 'us-west-2')
        results = {}
        
        for region in self.carbon_intensity_data.keys():
            if region != 'default':
                workload_copy = workload_data.copy()
                workload_copy['region'] = region
                
                analysis = self.analyze_comprehensive(workload_copy)
                if analysis['status'] == 'success':
                    results[region] = {
                        'carbon_savings_kg': analysis['carbon_analysis']['carbon_savings_kg'],
                        'cost_savings_usd': analysis['cost_analysis']['cost_savings_usd'],
                        'carbon_intensity': self.carbon_intensity_data[region],
                        'cost_per_hour': self.cost_data[region]
                    }
        
        # Sort by best carbon savings
        best_carbon = max(results.items(), key=lambda x: x[1]['carbon_savings_kg'])
        best_cost = max(results.items(), key=lambda x: x[1]['cost_savings_usd'])
        
        return {
            'region_comparison': results,
            'recommendations': {
                'best_for_carbon': best_carbon[0],
                'best_for_cost': best_cost[0],
                'current_region': original_region
            },
            'status': 'success'
        }

# Create global instance
carbon_calculator = CarbonCalculator()