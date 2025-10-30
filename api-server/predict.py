
import joblib
import pandas as pd
import json
import numpy as np

# Load model and encoders
model = joblib.load('carbon_model.pkl')
model_encoder = joblib.load('model_encoder.pkl')
gpu_encoder = joblib.load('gpu_encoder.pkl')
region_encoder = joblib.load('region_encoder.pkl')

with open('region_carbon.json', 'r') as f:
    REGION_CARBON = json.load(f)

def predict_carbon(model_type, batch_size, dataset_size_gb, gpu_count, gpu_type, duration_hours, region):
    """
    Predict carbon emissions for an ML job
    """
    # Encode categorical variables
    model_encoded = model_encoder.transform([model_type])[0]
    gpu_encoded = gpu_encoder.transform([gpu_type])[0]
    region_encoded = region_encoder.transform([region])[0]

    # Create input dataframe
    input_data = pd.DataFrame([{
        'model_type_encoded': model_encoded,
        'batch_size': batch_size,
        'dataset_size_gb': dataset_size_gb,
        'gpu_count': gpu_count,
        'gpu_type_encoded': gpu_encoded,
        'duration_hours': duration_hours,
        'region_encoded': region_encoded
    }])

    # Predict
    prediction = model.predict(input_data)[0]

    return float(prediction)

def find_greenest_region(model_type, batch_size, dataset_size_gb, gpu_count, gpu_type, duration_hours):
    """
    Find the greenest region for this job
    """
    results = {}
    for region in REGION_CARBON.keys():
        carbon = predict_carbon(model_type, batch_size, dataset_size_gb, gpu_count, gpu_type, duration_hours, region)
        results[region] = carbon

    greenest = min(results, key=results.get)
    return greenest, results

if __name__ == "__main__":
    # Test
    result = predict_carbon('ResNet50', 32, 100, 2, 'V100', 4.0, 'us-east-1')
    print(f"Predicted carbon: {result:.2f} kg CO2")
