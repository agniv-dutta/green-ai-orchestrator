import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from loguru import logger
from datetime import datetime, timedelta


class GreenAIOptimizationEngine:
    """Optimization engine for scheduling AI workloads during green energy windows"""
    
    def __init__(self):
        self.optimization_methods = {
            'carbon_aware': self._carbon_aware_scheduling,
            'balanced': self._balanced_scheduling,
            'fastest': self._fastest_scheduling
        }
    
    def optimize_schedule(self, workloads: List[Dict], carbon_forecast: pd.DataFrame,
                         optimization_strategy: str = 'carbon_aware') -> Dict[str, Any]:
        """Optimize workload schedule based on carbon forecast"""
        
        if optimization_strategy not in self.optimization_methods:
            raise ValueError(f"Unknown optimization strategy: {optimization_strategy}")
        
        return self.optimization_methods[optimization_strategy](workloads, carbon_forecast)
    
    def _carbon_aware_scheduling(self, workloads: List[Dict], 
                               carbon_forecast: pd.DataFrame) -> Dict[str, Any]:
        """Carbon-aware scheduling prioritizing green energy windows"""
        logger.info("Using carbon-aware scheduling strategy")
        
        carbon_values = carbon_forecast['carbon_intensity'].values
        schedule = []
        current_time = 0
        total_carbon = 0
        
        # Sort by priority and deadline
        sorted_workloads = sorted(workloads, key=lambda x: (x.get('priority', 3), x.get('deadline', 24)))
        
        for workload in sorted_workloads:
            deadline = min(workload.get('deadline', len(carbon_values)), len(carbon_values) - 1)
            available_slots = list(range(current_time, deadline + 1))
            
            if available_slots:
                # Find the greenest time slot
                best_slot = min(available_slots, key=lambda slot: carbon_values[slot])
                
                carbon_cost = carbon_values[best_slot] * workload.get('compute_requirements', 1.0)
                total_carbon += carbon_cost
                
                schedule.append({
                    **workload,
                    'scheduled_time_slot': best_slot,
                    'carbon_cost': carbon_cost,
                    'scheduling_method': 'carbon_aware'
                })
                
                current_time = best_slot + 1
            else:
                # Fallback: schedule at current time
                carbon_cost = carbon_values[current_time] * workload.get('compute_requirements', 1.0)
                total_carbon += carbon_cost
                
                schedule.append({
                    **workload,
                    'scheduled_time_slot': current_time,
                    'carbon_cost': carbon_cost,
                    'scheduling_method': 'fallback'
                })
                current_time += 1
        
        return {
            'schedule': schedule,
            'total_carbon': total_carbon,
            'strategy': 'carbon_aware',
            'workloads_scheduled': len(schedule)
        }
    
    def _balanced_scheduling(self, workloads: List[Dict],
                           carbon_forecast: pd.DataFrame) -> Dict[str, Any]:
        """Balanced scheduling considering both carbon and performance"""
        logger.info("Using balanced scheduling strategy")
        
        # This is a simplified version - in practice you might use weighted optimization
        return self._carbon_aware_scheduling(workloads, carbon_forecast)
    
    def _fastest_scheduling(self, workloads: List[Dict],
                          carbon_forecast: pd.DataFrame) -> Dict[str, Any]:
        """Schedule as fast as possible (baseline for comparison)"""
        logger.info("Using fastest scheduling strategy (baseline)")
        
        carbon_values = carbon_forecast['carbon_intensity'].values
        schedule = []
        current_time = 0
        total_carbon = 0
        
        for workload in workloads:
            carbon_cost = carbon_values[current_time] * workload.get('compute_requirements', 1.0)
            total_carbon += carbon_cost
            
            schedule.append({
                **workload,
                'scheduled_time_slot': current_time,
                'carbon_cost': carbon_cost,
                'scheduling_method': 'fastest'
            })
            current_time += 1
        
        return {
            'schedule': schedule,
            'total_carbon': total_carbon,
            'strategy': 'fastest',
            'workloads_scheduled': len(schedule)
        }
    
    def calculate_savings(self, baseline_schedule: List[Dict], 
                         optimized_schedule: List[Dict]) -> Dict[str, float]:
        """Calculate carbon savings from optimization"""
        
        baseline_carbon = sum(job.get('carbon_cost', 0) for job in baseline_schedule)
        optimized_carbon = sum(job.get('carbon_cost', 0) for job in optimized_schedule)
        
        if baseline_carbon == 0:
            return {'savings_percent': 0, 'savings_absolute': 0}
        
        savings_absolute = baseline_carbon - optimized_carbon
        savings_percent = (savings_absolute / baseline_carbon) * 100
        
        return {
            'savings_percent': savings_percent,
            'savings_absolute': savings_absolute,
            'baseline_carbon': baseline_carbon,
            'optimized_carbon': optimized_carbon
        }