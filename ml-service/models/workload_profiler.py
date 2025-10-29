import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Any
from loguru import logger
import joblib


class WorkloadProfiler:
    """Profiles AI workloads and predicts resource requirements"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.kmeans = None
        self.is_trained = False
        self.workload_types = {
            0: "Light Inference",
            1: "Heavy Inference", 
            2: "Model Training",
            3: "Fine-tuning",
            4: "Hyperparameter Optimization"
        }
    
    def extract_features(self, workload_data: pd.DataFrame) -> pd.DataFrame:
        """Extract features from workload data"""
        features = []
        
        for _, row in workload_data.iterrows():
            feature_vector = [
                row.get('cpu_usage', 0),
                row.get('memory_usage', 0),
                row.get('gpu_usage', 0),
                row.get('duration_minutes', 0),
                row.get('input_size_mb', 0),
                row.get('model_complexity', 0),  # Approx by model size/parameters
                row.get('batch_size', 1),
                row.get('throughput', 0)
            ]
            features.append(feature_vector)
        
        return pd.DataFrame(features, columns=[
            'cpu_usage', 'memory_usage', 'gpu_usage', 'duration',
            'input_size', 'model_complexity', 'batch_size', 'throughput'
        ])
    
    def train(self, historical_workloads: pd.DataFrame, n_clusters: int = 5):
        """Train workload profiling model"""
        logger.info("Training workload profiler")
        
        # Extract features
        features = self.extract_features(historical_workloads)
        
        # Scale features
        scaled_features = self.scaler.fit_transform(features)
        
        # Apply K-means clustering
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = self.kmeans.fit_predict(scaled_features)
        
        # Analyze clusters to define workload types
        self._analyze_clusters(features, clusters)
        
        self.is_trained = True
        logger.info("Workload profiler training completed")
    
    def _analyze_clusters(self, features: pd.DataFrame, clusters: np.ndarray):
        """Analyze clusters to understand workload types"""
        self.cluster_profiles = {}
        
        for cluster_id in range(self.kmeans.n_clusters):
            cluster_data = features[clusters == cluster_id]
            
            profile = {
                'avg_cpu': cluster_data['cpu_usage'].mean(),
                'avg_memory': cluster_data['memory_usage'].mean(),
                'avg_gpu': cluster_data['gpu_usage'].mean(),
                'avg_duration': cluster_data['duration'].mean(),
                'workload_type': self.workload_types.get(cluster_id, f"Type_{cluster_id}")
            }
            
            self.cluster_profiles[cluster_id] = profile
        
        logger.info(f"Created {len(self.cluster_profiles)} workload profiles")
    
    def predict_workload_type(self, workload_features: Dict[str, float]) -> Dict[str, Any]:
        """Predict workload type and resource requirements"""
        if not self.is_trained:
            raise ValueError("Profiler must be trained first")
        
        # Convert to feature vector
        feature_vector = [
            workload_features.get('cpu_usage', 0),
            workload_features.get('memory_usage', 0),
            workload_features.get('gpu_usage', 0),
            workload_features.get('duration_minutes', 0),
            workload_features.get('input_size_mb', 0),
            workload_features.get('model_complexity', 0),
            workload_features.get('batch_size', 1),
            workload_features.get('throughput', 0)
        ]
        
        # Scale features
        scaled_features = self.scaler.transform([feature_vector])
        
        # Predict cluster
        cluster_id = self.kmeans.predict(scaled_features)[0]
        profile = self.cluster_profiles[cluster_id]
        
        return {
            'workload_type': profile['workload_type'],
            'predicted_cpu': profile['avg_cpu'],
            'predicted_memory': profile['avg_memory'],
            'predicted_gpu': profile['avg_gpu'],
            'predicted_duration': profile['avg_duration'],
            'cluster_id': cluster_id
        }
    
    def estimate_carbon_footprint(self, workload_features: Dict[str, float], 
                                carbon_intensity: float) -> float:
        """Estimate carbon footprint for a workload"""
        prediction = self.predict_workload_type(workload_features)
        
        # Simplified carbon calculation
        energy_consumption = (
            prediction['predicted_cpu'] * 0.2 +  # CPU energy factor
            prediction['predicted_memory'] * 0.05 +  # Memory energy factor  
            prediction['predicted_gpu'] * 0.5  # GPU energy factor
        ) * (prediction['predicted_duration'] / 60)  # Convert to hours
        
        carbon_footprint = energy_consumption * carbon_intensity
        return carbon_footprint
    
    def save_model(self, filepath: str):
        """Save trained model"""
        joblib.dump({
            'scaler': self.scaler,
            'kmeans': self.kmeans,
            'cluster_profiles': self.cluster_profiles
        }, filepath)
        logger.info(f"Workload profiler saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model"""
        model_data = joblib.load(filepath)
        self.scaler = model_data['scaler']
        self.kmeans = model_data['kmeans']
        self.cluster_profiles = model_data['cluster_profiles']
        self.is_trained = True
        logger.info(f"Workload profiler loaded from {filepath}")