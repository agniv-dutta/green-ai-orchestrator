// Mock backend service for carbon calculations
const mockBackend = {
  // Get carbon intensity data for different regions
  getCarbonData: async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          'us-east-1': { region: 'US East (N. Virginia)', intensity: 0.38, source: 'EPA 2024' },
          'us-west-2': { region: 'US West (Oregon)', intensity: 0.28, source: 'EPA 2024' },
          'eu-west-1': { region: 'EU West (Ireland)', intensity: 0.32, source: 'EEA 2024' },
          'ap-southeast-1': { region: 'Asia Pacific (Singapore)', intensity: 0.48, source: 'Gov SG 2024' },
          'ca-central-1': { region: 'Canada (Central)', intensity: 0.12, source: 'Env Canada 2024' }
        });
      }, 500);
    });
  },

  // Refresh carbon data
  refreshCarbonData: async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          'us-east-1': { region: 'US East (N. Virginia)', intensity: 0.37, source: 'EPA 2024' },
          'us-west-2': { region: 'US West (Oregon)', intensity: 0.27, source: 'EPA 2024' },
          'eu-west-1': { region: 'EU West (Ireland)', intensity: 0.31, source: 'EEA 2024' },
          'ap-southeast-1': { region: 'Asia Pacific (Singapore)', intensity: 0.47, source: 'Gov SG 2024' },
          'ca-central-1': { region: 'Canada (Central)', intensity: 0.11, source: 'Env Canada 2024' }
        });
      }, 1000);
    });
  },

  // Predict carbon emissions
  predict: async (formData) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const baseCarbon = (formData.duration_hours * formData.gpu_count * 0.3) + 
                          (formData.dataset_size_gb * 0.01);
        
        const carbonByRegion = {
          'us-east-1': baseCarbon * 0.38,
          'us-west-2': baseCarbon * 0.28,
          'eu-west-1': baseCarbon * 0.32,
          'ap-southeast-1': baseCarbon * 0.48,
          'ca-central-1': baseCarbon * 0.12
        };

        const currentCarbon = carbonByRegion[formData.region];
        const greenestRegion = Object.entries(carbonByRegion)
          .sort(([,a], [,b]) => a - b)[0][0];
        const bestCarbon = carbonByRegion[greenestRegion];
        const savings = currentCarbon - bestCarbon;
        const savingsPercentage = ((savings / currentCarbon) * 100);

        resolve({
          predicted_carbon_kg: currentCarbon,
          carbon_by_region: carbonByRegion,
          greenest_region: greenestRegion,
          potential_savings_kg: savings,
          savings_percentage: savingsPercentage,
          region: formData.region,
          job_id: 'JOB_' + Math.random().toString(36).substr(2, 9).toUpperCase()
        });
      }, 1500);
    });
  },

  // Calculate estimated power
  calculateEstimatedPower: (formData) => {
    const modelPower = {
      'ResNet50': 180,
      'BERT-Base': 250,
      'GPT-2': 350,
      'ViT': 220,
      'YOLO': 150,
      'CNN-Small': 80
    };
    
    const gpuPower = {
      'T4': 70,
      'V100': 300,
      'A100': 400
    };
    
    return (modelPower[formData.model_type] || 200) + 
           (gpuPower[formData.gpu_type] || 250) * formData.gpu_count;
  },

  // Get dashboard stats
  getStats: async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          total_jobs: 47,
          total_carbon_predicted_kg: 125.6,
          total_potential_savings_kg: 42.3,
          average_savings_percentage: 33.7,
          jobs_by_region: {
            'us-east-1': 15,
            'us-west-2': 12,
            'eu-west-1': 10,
            'ap-southeast-1': 7,
            'ca-central-1': 3
          },
          jobs_by_model: {
            'ResNet50': 18,
            'BERT-Base': 12,
            'GPT-2': 8,
            'ViT': 5,
            'YOLO': 3,
            'CNN-Small': 1
          }
        });
      }, 800);
    });
  },

  // Get recent jobs
  getJobs: async (limit = 10) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const jobs = Array.from({ length: limit }, (_, i) => ({
          job_id: 'JOB_' + Math.random().toString(36).substr(2, 9).toUpperCase(),
          model_type: ['ResNet50', 'BERT-Base', 'GPT-2', 'ViT'][i % 4],
          region: ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1', 'ca-central-1'][i % 5],
          predicted_carbon_kg: 2.5 + Math.random() * 5,
          potential_savings_kg: 0.5 + Math.random() * 2,
          savings_percentage: 15 + Math.random() * 35
        }));
        resolve(jobs);
      }, 600);
    });
  }
};

export default mockBackend;