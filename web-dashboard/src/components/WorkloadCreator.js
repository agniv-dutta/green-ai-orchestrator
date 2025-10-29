import React, { useState } from 'react';
import { 
  Container, Row, Col, Card, Form, Button, Badge, 
  InputGroup, Alert
} from 'react-bootstrap';
import { 
  Cpu, MemoryStick, Gauge, Clock, Zap, CheckCircle, 
  Cloud, Brain, Database 
} from 'lucide-react';

const WorkloadCreator = ({ onWorkloadCreated }) => {
  const [workloadData, setWorkloadData] = useState({
    name: 'Image Classification Training',
    workload_type: 'model_training',
    cpu_cores: 4,
    memory_gb: 16,
    gpu_count: 1,
    duration_hours: 2,
    dataset_size: 50
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const workloadTypes = [
    { value: 'model_training', label: 'Model Training', icon: Brain, description: 'Train machine learning models' },
    { value: 'inference', label: 'Model Inference', icon: Gauge, description: 'Run model predictions' },
    { value: 'data_processing', label: 'Data Processing', icon: Database, description: 'Process and transform data' },
    { value: 'hyperparameter_tuning', label: 'Hyperparameter Tuning', icon: Zap, description: 'Optimize model parameters' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setWorkloadData(prev => ({
      ...prev,
      [name]: name === 'workload_type' ? value : 
              name === 'name' ? value : parseFloat(value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // Simulate workload optimization
      const optimizedConfig = await optimizeWorkload(workloadData);
      setResult(optimizedConfig);
      onWorkloadCreated();
    } catch (err) {
      setError('Failed to optimize workload. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const optimizeWorkload = async (workload) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        // Simulate AI optimization
        const baseCarbon = (workload.cpu_cores * 0.1) + (workload.memory_gb * 0.05) + 
                          (workload.gpu_count * 0.5) + (workload.duration_hours * 0.2);
        
        const optimized = {
          ...workload,
          optimized_cpu_cores: Math.max(2, Math.floor(workload.cpu_cores * 0.8)),
          optimized_memory_gb: Math.max(8, Math.floor(workload.memory_gb * 0.9)),
          optimized_gpu_count: Math.max(1, Math.floor(workload.gpu_count)),
          estimated_carbon: baseCarbon,
          optimized_carbon: baseCarbon * 0.7, // 30% reduction
          recommended_region: 'us-west-2',
          cost_savings: 25,
          carbon_savings: 30
        };
        
        resolve(optimized);
      }, 1500);
    });
  };

  const getWorkloadTypeIcon = (type) => {
    const workloadType = workloadTypes.find(wt => wt.value === type);
    const IconComponent = workloadType ? workloadType.icon : Brain;
    return <IconComponent size={20} />;
  };

  return (
    <Container id="workload-creator" className="my-5">
      <Row className="justify-content-center">
        <Col lg={8}>
          <Card className="card-hover border-0">
            <Card.Header className="gradient-bg text-white py-4">
              <div className="d-flex align-items-center">
                <Brain size={24} className="me-2" />
                <h4 className="mb-0 fw-bold">Create AI Workload</h4>
              </div>
              <p className="mb-0 mt-2 opacity-75">
                Let our ML engine optimize your cloud resource allocation
              </p>
            </Card.Header>
            
            <Card.Body className="p-4">
              <Form onSubmit={handleSubmit}>
                {/* Workload Name */}
                <Row className="mb-4">
                  <Col>
                    <Form.Group>
                      <Form.Label className="fw-semibold text-dark mb-3">
                        Workload Name
                      </Form.Label>
                      <Form.Control
                        type="text"
                        name="name"
                        value={workloadData.name}
                        onChange={handleInputChange}
                        placeholder="e.g., Image Classification Training"
                        className="border-2 py-3"
                        required
                      />
                    </Form.Group>
                  </Col>
                </Row>

                {/* Workload Type */}
                <Row className="mb-4">
                  <Col>
                    <Form.Label className="fw-semibold text-dark mb-3">
                      Workload Type
                    </Form.Label>
                    <div className="row g-3">
                      {workloadTypes.map((type) => (
                        <Col key={type.value} md={6}>
                          <div 
                            className={`p-3 border rounded-3 cursor-pointer transition-all ${
                              workloadData.workload_type === type.value 
                                ? 'border-success bg-success bg-opacity-10' 
                                : 'border-light'
                            }`}
                            onClick={() => setWorkloadData(prev => ({
                              ...prev,
                              workload_type: type.value
                            }))}
                            style={{ cursor: 'pointer' }}
                          >
                            <div className="d-flex align-items-center">
                              <type.icon 
                                size={20} 
                                className={`me-2 ${
                                  workloadData.workload_type === type.value 
                                    ? 'text-success' 
                                    : 'text-muted'
                                }`} 
                              />
                              <div>
                                <div className="fw-semibold">
                                  {type.label}
                                  {workloadData.workload_type === type.value && (
                                    <CheckCircle size={16} className="text-success ms-2" />
                                  )}
                                </div>
                                <small className="text-muted">{type.description}</small>
                              </div>
                            </div>
                          </div>
                        </Col>
                      ))}
                    </div>
                  </Col>
                </Row>

                {/* Resource Configuration */}
                <Row className="g-4 mb-4">
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold text-dark mb-3">
                        <Cpu size={18} className="me-2 text-primary" />
                        CPU Cores
                      </Form.Label>
                      <InputGroup>
                        <Form.Control
                          type="number"
                          name="cpu_cores"
                          value={workloadData.cpu_cores}
                          onChange={handleInputChange}
                          min="1"
                          max="64"
                          className="border-2 py-3"
                        />
                        <InputGroup.Text className="bg-light border-2">
                          Cores
                        </InputGroup.Text>
                      </InputGroup>
                    </Form.Group>
                  </Col>

                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold text-dark mb-3">
                        <MemoryStick size={18} className="me-2 text-info" />
                        Memory (GB)
                      </Form.Label>
                      <InputGroup>
                        <Form.Control
                          type="number"
                          name="memory_gb"
                          value={workloadData.memory_gb}
                          onChange={handleInputChange}
                          min="1"
                          max="512"
                          className="border-2 py-3"
                        />
                        <InputGroup.Text className="bg-light border-2">
                          GB
                        </InputGroup.Text>
                      </InputGroup>
                    </Form.Group>
                  </Col>

                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold text-dark mb-3">
                        <Gauge size={18} className="me-2 text-warning" />
                        GPU Count
                      </Form.Label>
                      <InputGroup>
                        <Form.Control
                          type="number"
                          name="gpu_count"
                          value={workloadData.gpu_count}
                          onChange={handleInputChange}
                          min="0"
                          max="8"
                          className="border-2 py-3"
                        />
                        <InputGroup.Text className="bg-light border-2">
                          GPUs
                        </InputGroup.Text>
                      </InputGroup>
                    </Form.Group>
                  </Col>

                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold text-dark mb-3">
                        <Clock size={18} className="me-2 text-success" />
                        Duration (hours)
                      </Form.Label>
                      <InputGroup>
                        <Form.Control
                          type="number"
                          name="duration_hours"
                          value={workloadData.duration_hours}
                          onChange={handleInputChange}
                          min="0.5"
                          max="168"
                          step="0.5"
                          className="border-2 py-3"
                        />
                        <InputGroup.Text className="bg-light border-2">
                          Hours
                        </InputGroup.Text>
                      </InputGroup>
                    </Form.Group>
                  </Col>
                </Row>

                {/* Dataset Size */}
                <Row className="mb-4">
                  <Col>
                    <Form.Group>
                      <Form.Label className="fw-semibold text-dark mb-3">
                        <Database size={18} className="me-2 text-secondary" />
                        Dataset Size (GB)
                      </Form.Label>
                      <Form.Range
                        name="dataset_size"
                        value={workloadData.dataset_size}
                        onChange={handleInputChange}
                        min="1"
                        max="1000"
                        className="mb-2"
                      />
                      <div className="d-flex justify-content-between align-items-center">
                        <small>1 GB</small>
                        <Badge bg="success" className="fs-6">
                          {workloadData.dataset_size} GB
                        </Badge>
                        <small>1000 GB</small>
                      </div>
                    </Form.Group>
                  </Col>
                </Row>

                {/* Submit Button */}
                <Row>
                  <Col>
                    <Button 
                      variant="success" 
                      type="submit" 
                      disabled={loading || !workloadData.name}
                      className="w-100 py-3 fw-bold fs-5"
                    >
                      {loading ? (
                        <>
                          <div className="spinner-border spinner-border-sm me-2" />
                          Optimizing Workload...
                        </>
                      ) : (
                        <>
                          <Zap size={20} className="me-2" />
                          Optimize & Create
                        </>
                      )}
                    </Button>
                  </Col>
                </Row>
              </Form>

              {/* Error Alert */}
              {error && (
                <Alert variant="danger" className="mt-4">
                  <Alert.Heading>Optimization Error</Alert.Heading>
                  {error}
                </Alert>
              )}

              {/* Optimization Results */}
              {result && (
                <div className="mt-4 p-4 bg-light rounded-3 border">
                  <h5 className="fw-bold text-success mb-3">
                    <CheckCircle size={20} className="me-2" />
                    Workload Optimized Successfully!
                  </h5>
                  
                  <Row className="g-3">
                    <Col md={6}>
                      <Card className="border-0 bg-white">
                        <Card.Body>
                          <h6 className="fw-semibold mb-3">Original Configuration</h6>
                          <div className="small">
                            <div>CPU: {workloadData.cpu_cores} cores</div>
                            <div>Memory: {workloadData.memory_gb} GB</div>
                            <div>GPU: {workloadData.gpu_count} units</div>
                            <div className="fw-bold mt-2">
                              Estimated Carbon: {result.estimated_carbon.toFixed(2)} kg CO₂
                            </div>
                          </div>
                        </Card.Body>
                      </Card>
                    </Col>
                    
                    <Col md={6}>
                      <Card className="border-0 bg-success text-white">
                        <Card.Body>
                          <h6 className="fw-semibold mb-3">Optimized Configuration</h6>
                          <div className="small">
                            <div>CPU: {result.optimized_cpu_cores} cores</div>
                            <div>Memory: {result.optimized_memory_gb} GB</div>
                            <div>GPU: {result.optimized_gpu_count} units</div>
                            <div className="fw-bold mt-2">
                              Optimized Carbon: {result.optimized_carbon.toFixed(2)} kg CO₂
                            </div>
                          </div>
                        </Card.Body>
                      </Card>
                    </Col>
                    
                    <Col md={12}>
                      <Alert variant="success" className="mb-0">
                        <Alert.Heading className="h6">
                          🎉 Optimization Results
                        </Alert.Heading>
                        <div className="row">
                          <div className="col">
                            <strong>Carbon Savings:</strong> {result.carbon_savings}%
                          </div>
                          <div className="col">
                            <strong>Cost Savings:</strong> {result.cost_savings}%
                          </div>
                          <div className="col">
                            <strong>Recommended Region:</strong> {result.recommended_region}
                          </div>
                        </div>
                      </Alert>
                    </Col>
                  </Row>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default WorkloadCreator;