import React, { useState, useEffect } from 'react';
import { 
  Container, Row, Col, Card, Form, Button, Alert, Badge, 
  Tooltip, OverlayTrigger, Spinner 
} from 'react-bootstrap';
import { Calculator, TrendingDown, MapPin, Leaf, Zap, Info, RefreshCw } from 'lucide-react';
import mockBackend from '../services/mockBackend';

const CarbonCalculator = ({ onNewPrediction }) => {
  const [formData, setFormData] = useState({
    model_type: 'ResNet50',
    batch_size: 32,
    dataset_size_gb: 100,
    gpu_count: 2,
    gpu_type: 'V100',
    duration_hours: 4.0,
    region: 'us-east-1'
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [carbonData, setCarbonData] = useState({});
  const [updatingCarbon, setUpdatingCarbon] = useState(false);

  const modelOptions = [
    { value: 'ResNet50', label: 'ResNet50', power: 180, params: '25M' },
    { value: 'BERT-Base', label: 'BERT-Base', power: 250, params: '110M' },
    { value: 'GPT-2', label: 'GPT-2', power: 350, params: '117M' },
    { value: 'ViT', label: 'Vision Transformer', power: 220, params: '86M' },
    { value: 'YOLO', label: 'YOLOv5', power: 150, params: '7M' },
    { value: 'CNN-Small', label: 'Small CNN', power: 80, params: '1M' }
  ];

  const gpuOptions = [
    { value: 'T4', label: 'NVIDIA T4', power: 70, memory: '16GB' },
    { value: 'V100', label: 'NVIDIA V100', power: 300, memory: '32GB' },
    { value: 'A100', label: 'NVIDIA A100', power: 400, memory: '80GB' }
  ];

  // Load carbon data on component mount
  useEffect(() => {
    loadCarbonData();
  }, []);

  const loadCarbonData = async () => {
    try {
      const data = await mockBackend.getCarbonData();
      setCarbonData(data);
    } catch (err) {
      console.error('Failed to load carbon data:', err);
      setError('Failed to load carbon intensity data');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'model_type' || name === 'gpu_type' || name === 'region' 
        ? value 
        : parseFloat(value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await mockBackend.predict(formData);
      setResult(response);
      onNewPrediction();
    } catch (err) {
      setError(err.message || 'Failed to calculate carbon emissions.');
    } finally {
      setLoading(false);
    }
  };

  const refreshCarbonData = async () => {
    setUpdatingCarbon(true);
    try {
      const data = await mockBackend.refreshCarbonData();
      setCarbonData(data);
    } catch (err) {
      console.error('Failed to refresh carbon data:', err);
    } finally {
      setUpdatingCarbon(false);
    }
  };

  const getTooltip = (text) => (
    <Tooltip>{text}</Tooltip>
  );

  const calculateEstimatedPower = () => {
    return mockBackend.calculateEstimatedPower(formData);
  };

  const getCarbonIntensityColor = (intensity) => {
    if (intensity < 0.3) return 'success';
    if (intensity < 0.5) return 'warning';
    return 'danger';
  };

  return (
    <Container id="calculator" className="my-5">
      <Row className="justify-content-center">
        <Col lg={10}>
          <Card className="card-hover border-0">
            <Card.Header className="gradient-bg text-white py-3">
              <div className="d-flex align-items-center justify-content-between">
                <div className="d-flex align-items-center">
                  <Calculator size={24} className="me-2" />
                  <h4 className="mb-0 fw-bold">Carbon Emission Calculator</h4>
                </div>
                <Button 
                  variant="outline-light" 
                  size="sm" 
                  onClick={refreshCarbonData}
                  disabled={updatingCarbon}
                >
                  {updatingCarbon ? (
                    <Spinner animation="border" size="sm" className="me-2" />
                  ) : (
                    <RefreshCw size={16} className="me-2" />
                  )}
                  Update Carbon Data
                </Button>
              </div>
            </Card.Header>
            <Card.Body className="p-4">
              {/* Real-time Carbon Intensity Display */}
              {Object.keys(carbonData).length > 0 && (
                <Card className="mb-4 border-0 bg-light">
                  <Card.Body className="py-3">
                    <h6 className="fw-bold mb-3">🌍 Real-time Carbon Intensity (kg CO₂/kWh)</h6>
                    <Row className="g-2">
                      {Object.entries(carbonData).map(([region, data]) => (
                        <Col key={region} xs={6} md={4} lg={2.4}>
                          <div className={`text-center p-2 rounded border ${
                            region === formData.region ? 'border-primary bg-white' : 'border-light'
                          }`}>
                            <div className="fw-bold fs-6">{data.intensity.toFixed(2)}</div>
                            <small className={`text-${getCarbonIntensityColor(data.intensity)}`}>
                              {data.region.split(' ')[0]}
                            </small>
                            <br />
                            <small className="text-muted">{data.source}</small>
                          </div>
                        </Col>
                      ))}
                    </Row>
                  </Card.Body>
                </Card>
              )}

              <Form onSubmit={handleSubmit}>
                <Row className="g-3">
                  {/* Model Type */}
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold">
                        Model Type
                        <OverlayTrigger placement="top" overlay={getTooltip("Select your machine learning model architecture")}>
                          <Info size={16} className="ms-1 text-muted" />
                        </OverlayTrigger>
                      </Form.Label>
                      <Form.Select 
                        name="model_type" 
                        value={formData.model_type}
                        onChange={handleInputChange}
                        className="border-2"
                      >
                        {modelOptions.map(model => (
                          <option key={model.value} value={model.value}>
                            {model.label} (~{model.power}W)
                          </option>
                        ))}
                      </Form.Select>
                    </Form.Group>
                  </Col>

                  {/* Batch Size */}
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold">
                        Batch Size
                        <OverlayTrigger placement="top" overlay={getTooltip("Number of samples processed in one iteration")}>
                          <Info size={16} className="ms-1 text-muted" />
                        </OverlayTrigger>
                      </Form.Label>
                      <Form.Range
                        name="batch_size"
                        value={formData.batch_size}
                        onChange={handleInputChange}
                        min="8"
                        max="128"
                        step="8"
                        className="mb-2"
                      />
                      <div className="d-flex justify-content-between">
                        <small>8</small>
                        <Badge bg="success">{formData.batch_size}</Badge>
                        <small>128</small>
                      </div>
                    </Form.Group>
                  </Col>

                  {/* Dataset Size */}
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold">
                        Dataset Size (GB)
                        <OverlayTrigger placement="top" overlay={getTooltip("Total size of your training dataset")}>
                          <Info size={16} className="ms-1 text-muted" />
                        </OverlayTrigger>
                      </Form.Label>
                      <Form.Control
                        type="number"
                        name="dataset_size_gb"
                        value={formData.dataset_size_gb}
                        onChange={handleInputChange}
                        min="1"
                        max="1000"
                        className="border-2"
                      />
                    </Form.Group>
                  </Col>

                  {/* GPU Configuration */}
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold">
                        GPU Type
                        <OverlayTrigger placement="top" overlay={getTooltip("Select your GPU hardware")}>
                          <Info size={16} className="ms-1 text-muted" />
                        </OverlayTrigger>
                      </Form.Label>
                      <Form.Select 
                        name="gpu_type" 
                        value={formData.gpu_type}
                        onChange={handleInputChange}
                        className="border-2"
                      >
                        {gpuOptions.map(gpu => (
                          <option key={gpu.value} value={gpu.value}>
                            {gpu.label} ({gpu.power}W each)
                          </option>
                        ))}
                      </Form.Select>
                    </Form.Group>
                  </Col>

                  {/* GPU Count */}
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold">
                        GPU Count
                        <OverlayTrigger placement="top" overlay={getTooltip("Number of GPUs used for training")}>
                          <Info size={16} className="ms-1 text-muted" />
                        </OverlayTrigger>
                      </Form.Label>
                      <Form.Range
                        name="gpu_count"
                        value={formData.gpu_count}
                        onChange={handleInputChange}
                        min="1"
                        max="8"
                        className="mb-2"
                      />
                      <div className="d-flex justify-content-between">
                        <small>1</small>
                        <Badge bg="success">{formData.gpu_count}</Badge>
                        <small>8</small>
                      </div>
                    </Form.Group>
                  </Col>

                  {/* Duration */}
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label className="fw-semibold">
                        Duration (Hours)
                        <OverlayTrigger placement="top" overlay={getTooltip("Estimated training time in hours")}>
                          <Info size={16} className="ms-1 text-muted" />
                        </OverlayTrigger>
                      </Form.Label>
                      <Form.Control
                        type="number"
                        name="duration_hours"
                        value={formData.duration_hours}
                        onChange={handleInputChange}
                        step="0.5"
                        min="0.5"
                        max="168"
                        className="border-2"
                      />
                    </Form.Group>
                  </Col>

                  {/* Region */}
                  <Col md={12}>
                    <Form.Group>
                      <Form.Label className="fw-semibold">
                        Cloud Region
                        <OverlayTrigger placement="top" overlay={getTooltip("Select your cloud provider region - carbon intensity varies by location")}>
                          <Info size={16} className="ms-1 text-muted" />
                        </OverlayTrigger>
                      </Form.Label>
                      <Form.Select 
                        name="region" 
                        value={formData.region}
                        onChange={handleInputChange}
                        className="border-2"
                      >
                        {Object.entries(carbonData).map(([key, data]) => (
                          <option key={key} value={key}>
                            {data.region} ({data.intensity.toFixed(2)} kg CO₂/kWh - {data.source})
                          </option>
                        ))}
                      </Form.Select>
                    </Form.Group>
                  </Col>

                  {/* Power Estimate */}
                  <Col md={12}>
                    <Card className="bg-light border-0">
                      <Card.Body className="py-2">
                        <div className="d-flex justify-content-between align-items-center">
                          <small className="fw-semibold">Estimated Power Consumption:</small>
                          <Badge bg="secondary" className="fs-6">
                            {calculateEstimatedPower()} Watts
                          </Badge>
                        </div>
                      </Card.Body>
                    </Card>
                  </Col>

                  {/* Submit Button */}
                  <Col md={12}>
                    <Button 
                      variant="success" 
                      type="submit" 
                      disabled={loading}
                      className="w-100 py-3 fw-bold fs-5"
                    >
                      {loading ? (
                        <>
                          <Spinner animation="border" size="sm" className="me-2" />
                          Calculating Carbon Emissions...
                        </>
                      ) : (
                        <>
                          <Calculator size={20} className="me-2" />
                          Calculate Carbon Footprint
                        </>
                      )}
                    </Button>
                  </Col>
                </Row>
              </Form>

              {/* Error Alert */}
              {error && (
                <Alert variant="danger" className="mt-3">
                  <Alert.Heading>Calculation Error</Alert.Heading>
                  {error}
                </Alert>
              )}

              {/* Results Section */}
              {result && (
                <div className="mt-4 result-highlight rounded p-4">
                  <Row className="g-3">
                    <Col md={12}>
                      <h5 className="fw-bold text-success mb-3">
                        <Zap size={20} className="me-2" />
                        Carbon Analysis Results
                      </h5>
                    </Col>

                    {/* Current Carbon */}
                    <Col md={3}>
                      <Card className="stat-card h-100 border-0 bg-white">
                        <Card.Body className="text-center">
                          <MapPin size={24} className="text-primary mb-2" />
                          <h4 className="fw-bold text-primary">{result.predicted_carbon_kg.toFixed(2)} kg</h4>
                          <small className="text-muted">Current in {result.region}</small>
                        </Card.Body>
                      </Card>
                    </Col>

                    {/* Greenest Region */}
                    <Col md={3}>
                      <Card className="stat-card h-100 border-0 bg-success text-white">
                        <Card.Body className="text-center">
                          <TrendingDown size={24} className="mb-2" />
                          <h4 className="fw-bold">{result.carbon_by_region[result.greenest_region].toFixed(2)} kg</h4>
                          <small>Best: {result.greenest_region}</small>
                        </Card.Body>
                      </Card>
                    </Col>

                    {/* Potential Savings */}
                    <Col md={3}>
                      <Card className="stat-card h-100 border-0 bg-warning text-dark">
                        <Card.Body className="text-center">
                          <Leaf size={24} className="mb-2" />
                          <h4 className="fw-bold">{result.potential_savings_kg.toFixed(2)} kg</h4>
                          <small>Potential Savings</small>
                        </Card.Body>
                      </Card>
                    </Col>

                    {/* Savings Percentage */}
                    <Col md={3}>
                      <Card className="stat-card h-100 border-0 bg-info text-white">
                        <Card.Body className="text-center">
                          <Zap size={24} className="mb-2" />
                          <h4 className="fw-bold">{result.savings_percentage.toFixed(1)}%</h4>
                          <small>Reduction</small>
                        </Card.Body>
                      </Card>
                    </Col>

                    {/* Recommendation */}
                    <Col md={12}>
                      <Alert variant="success" className="mb-0">
                        <Alert.Heading className="h6">
                          💡 Optimization Recommendation
                        </Alert.Heading>
                        Switch from <strong>{result.region}</strong> to <strong>{result.greenest_region}</strong> to save{' '}
                        <strong>{result.potential_savings_kg.toFixed(2)} kg CO₂</strong> ({result.savings_percentage.toFixed(1)}% reduction)
                      </Alert>
                    </Col>

                    {/* Region Comparison */}
                    <Col md={12}>
                      <h6 className="fw-semibold mb-3">Carbon Emissions by Region:</h6>
                      <Row className="g-2">
                        {Object.entries(result.carbon_by_region)
                          .sort(([,a], [,b]) => a - b)
                          .map(([region, carbon]) => (
                            <Col key={region} md={2} sm={4} xs={6}>
                              <Card className={`
                                h-100 text-center p-2 
                                ${region === result.greenest_region ? 'region-best' : ''}
                                ${region === result.region ? 'region-current' : 'bg-light'}
                              `}>
                                <Card.Body className="p-2">
                                  <div className="fw-bold fs-6">{carbon.toFixed(2)} kg</div>
                                  <small className="text-muted">{region.split('-')[0]}</small>
                                </Card.Body>
                              </Card>
                            </Col>
                          ))}
                      </Row>
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

export default CarbonCalculator;