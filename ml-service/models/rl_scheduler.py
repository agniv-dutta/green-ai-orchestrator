import gym
from gym import spaces
import numpy as np
import torch
import torch.nn as nn
from loguru import logger
from typing import Dict, List, Any
import pandas as pd

# Ray/RLlib is optional - we'll use rule-based scheduling
RAY_AVAILABLE = False
logger.info("Using efficient rule-based scheduling")

class GreenAISchedulingEnv:
    """Simplified environment for rule-based scheduling"""
    
    def __init__(self, config: Dict[str, Any]):
        self.carbon_data = config.get('carbon_data', [])
        self.workload_queue = config.get('workload_queue', [])
        self.scheduled_workloads = []
    
    def reset(self):
        self.scheduled_workloads = []
        return np.zeros(10)  # Dummy observation
    
    def step(self, action):
        # Not used in rule-based scheduling
        return np.zeros(10), 0, True, {}


class RLWorkloadScheduler:
    """Workload scheduler using efficient rule-based algorithms"""
    
    def __init__(self):
        self.is_trained = True  # Rule-based is always "trained"
        logger.info("Initialized rule-based workload scheduler")
    
    def train(self, carbon_data: List[float], training_iterations: int = 1000) -> Dict:
        """Rule-based scheduler doesn't need training"""
        logger.info("Rule-based scheduler ready to use")
        return {
            'status': 'rule_based_ready',
            'message': 'Using carbon-aware rule-based scheduling'
        }
    
    def schedule_workloads(self, workloads: List[Dict], carbon_forecast: List[float]) -> List[Dict]:
        """Schedule workloads using carbon-aware rules"""
        logger.info(f"Scheduling {len(workloads)} workloads using rule-based algorithm")
        
        if not workloads:
            return []
        
        scheduled = []
        current_time = 0
        
        # Sort by priority (ascending) and deadline (ascending)
        sorted_workloads = sorted(workloads, key=lambda x: (
            x.get('priority', 3), 
            x.get('deadline', 24)
        ))
        
        for workload in sorted_workloads:
            deadline = min(workload.get('deadline', 24), len(carbon_forecast) - 1)
            
            # Find available time slots
            available_slots = list(range(current_time, deadline + 1))
            
            if available_slots:
                # Find the greenest time slot (lowest carbon intensity)
                best_slot = min(available_slots, key=lambda slot: carbon_forecast[slot])
                
                # Calculate carbon cost
                carbon_cost = carbon_forecast[best_slot] * workload.get('compute_requirements', 1.0)
                
                scheduled.append({
                    **workload,
                    'scheduled_time_slot': best_slot,
                    'carbon_cost': carbon_cost,
                    'scheduling_method': 'carbon_aware_rule_based'
                })
                
                # Move current time forward
                current_time = best_slot + 1
            else:
                # Schedule at current time if no slots available
                scheduled.append({
                    **workload,
                    'scheduled_time_slot': current_time,
                    'carbon_cost': carbon_forecast[current_time] * workload.get('compute_requirements', 1.0),
                    'scheduling_method': 'fallback'
                })
                current_time += 1
        
        # Calculate total carbon savings
        baseline_carbon = self._calculate_baseline_carbon(workloads, carbon_forecast)
        optimized_carbon = sum(job['carbon_cost'] for job in scheduled)
        savings = baseline_carbon - optimized_carbon
        
        logger.info(f"Scheduled {len(scheduled)} workloads. Carbon savings: {savings:.2f}")
        
        return scheduled
    
    def _calculate_baseline_carbon(self, workloads: List[Dict], carbon_forecast: List[float]) -> float:
        """Calculate carbon cost if all workloads were scheduled immediately"""
        total = 0
        current_time = 0
        
        for workload in workloads:
            carbon_cost = carbon_forecast[current_time] * workload.get('compute_requirements', 1.0)
            total += carbon_cost
            current_time += 1
        
        return total
    
    def save_model(self, filepath: str):
        """Rule-based doesn't need saving"""
        logger.info("Rule-based scheduler doesn't require model saving")
    
    def load_model(self, filepath: str):
        """Rule-based doesn't need loading"""
        logger.info("Rule-based scheduler doesn't require model loading")