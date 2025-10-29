import React, { useState, useEffect } from 'react';
import { 
  Container, Row, Col, Card, Table, Badge, Spinner, Alert, Button 
} from 'react-bootstrap';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Activity, Database, TrendingUp, Zap, Users, Cloud, RefreshCw } from 'lucide-react';
import mockBackend from '../services/mockBackend';

const Dashboard = ({ refreshTrigger }) => {
  const [stats, setStats] = useState(null);
  const [recentJobs, setRecentJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [carbonData, setCarbonData] = useState({});

  const fetchData = async () => {
    try {
      setError('');
      const [statsResponse, jobsResponse, carbonResponse] = await Promise.all([
        mockBackend.getStats(),
        mockBackend.getJobs(10),
        mockBackend.getCarbonData()
      ]);
      
      setStats(statsResponse);
      setRecentJobs(jobsResponse);
      setCarbonData(carbonResponse);
    } catch (err) {
      setError('Failed to load dashboard data.');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [refreshTrigger]);

  const COLORS = ['#22c55e', '#3b82f6', '#ef4444', '#f59e0b', '#8b5cf6', '#ec4899'];

  if (loading) {
    return (
      <Container className="my-5 text-center">
        <Spinner animation="border" variant="success" style={{ width: '3rem', height: '3rem' }} />
        <p className="mt-3 text-muted">Loading dashboard data...</p>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="my-5">
        <Alert variant="warning">
          <Alert.Heading>Dashboard Unavailable</Alert.Heading>
          {error}
          <hr />
          <div className="d-flex justify-content-between">
            <small>Try refreshing the data</small>
            <Button variant="outline-success" size="sm" onClick={fetchData}>
              Retry
            </Button>
          </div>
        </Alert>
      </Container>
    );
  }

  if (!stats) {
    return (
      <Container className="my-5">
        <Alert variant="info">
          No data available. Run some carbon calculations first!
        </Alert>
      </Container>
    );
  }

  const regionData = Object.entries(stats.jobs_by_region).map(([name, value]) => ({
    name: name.split('-')[0],
    value,
    fullName: name
  }));

  const modelData = Object.entries(stats.jobs_by_model).map(([name, value]) => ({
    name,
    value
  }));

  const carbonIntensityData = Object.entries(carbonData).map(([key, data]) => ({
    name: key.split('-')[0],
    intensity: data.intensity,
    source: data.source
  }));

  return (
    <Container id="dashboard" className="my-5">
      <Row className="mb-4">
        <Col>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h2 className="fw-bold">
                <Activity className="me-2" />
                Live Carbon Analytics Dashboard
              </h2>
              <p className="text-muted mb-0">
                Real-time insights into your ML carbon footprint and optimization opportunities
              </p>
            </div>
            <Button variant="outline-success" onClick={fetchData}>
              <RefreshCw size={16} className="me-2" />
              Refresh
            </Button>
          </div>
        </Col>
      </Row>

      {/* Stats Overview */}
      <Row className="g-4 mb-4">
        <Col md={3} sm={6}>
          <Card className="stat-card border-0 bg-primary text-white">
            <Card.Body>
              <div className="d-flex align-items-center">
                <Database size={32} className="me-3" />
                <div>
                  <h4 className="fw-bold mb-0">{stats.total_jobs}</h4>
                  <small>Total Jobs Analyzed</small>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3} sm={6}>
          <Card className="stat-card border-0 bg-success text-white">
            <Card.Body>
              <div className="d-flex align-items-center">
                <Activity size={32} className="me-3" />
                <div>
                  <h4 className="fw-bold mb-0">{stats.total_carbon_predicted_kg.toFixed(1)} kg</h4>
                  <small>Carbon Predicted</small>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3} sm={6}>
          <Card className="stat-card border-0 bg-warning text-dark">
            <Card.Body>
              <div className="d-flex align-items-center">
                <Zap size={32} className="me-3" />
                <div>
                  <h4 className="fw-bold mb-0">{stats.total_potential_savings_kg.toFixed(1)} kg</h4>
                  <small>Potential Savings</small>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>

        <Col md={3} sm={6}>
          <Card className="stat-card border-0 bg-info text-white">
            <Card.Body>
              <div className="d-flex align-items-center">
                <TrendingUp size={32} className="me-3" />
                <div>
                  <h4 className="fw-bold mb-0">{stats.average_savings_percentage.toFixed(1)}%</h4>
                  <small>Average Savings</small>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Charts Section */}
      <Row className="g-4 mb-4">
        <Col lg={4} md={6}>
          <Card className="chart-container border-0 h-100">
            <Card.Header className="bg-transparent border-0">
              <h6 className="fw-bold mb-0">
                <Users size={16} className="me-2" />
                Jobs by Region
              </h6>
            </Card.Header>
            <Card.Body>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={regionData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {regionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value, name) => [value, 'Jobs']} />
                </PieChart>
              </ResponsiveContainer>
            </Card.Body>
          </Card>
        </Col>

        <Col lg={4} md={6}>
          <Card className="chart-container border-0 h-100">
            <Card.Header className="bg-transparent border-0">
              <h6 className="fw-bold mb-0">
                <Cloud size={16} className="me-2" />
                Jobs by Model
              </h6>
            </Card.Header>
            <Card.Body>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={modelData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={60} fontSize={12} />
                  <YAxis fontSize={12} />
                  <Tooltip />
                  <Bar dataKey="value" fill="#22c55e" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </Card.Body>
          </Card>
        </Col>

        <Col lg={4} md={12}>
          <Card className="chart-container border-0 h-100">
            <Card.Header className="bg-transparent border-0">
              <h6 className="fw-bold mb-0">
                <TrendingUp size={16} className="me-2" />
                Carbon Intensity
              </h6>
            </Card.Header>
            <Card.Body>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={carbonIntensityData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="name" fontSize={12} />
                  <YAxis fontSize={12} />
                  <Tooltip formatter={(value) => [`${value} kg/kWh`, 'Intensity']} />
                  <Bar dataKey="intensity" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
              <div className="text-center mt-2">
                <Badge bg="success" className="me-1">Low: {'<0.3'}</Badge>
                <Badge bg="warning" className="me-1">Medium: 0.3-0.5</Badge>
                <Badge bg="danger">High: {'>0.5'}</Badge>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Recent Jobs Table */}
      <Row>
        <Col>
          <Card className="border-0">
            <Card.Header className="gradient-bg text-white">
              <h5 className="mb-0 fw-bold">
                <Activity size={20} className="me-2" />
                Recent Carbon Predictions
              </h5>
            </Card.Header>
            <Card.Body className="p-0">
              <Table hover responsive className="mb-0">
                <thead className="bg-light">
                  <tr>
                    <th>Job ID</th>
                    <th>Model</th>
                    <th>Region</th>
                    <th className="text-end">Carbon (kg)</th>
                    <th className="text-end">Savings (kg)</th>
                    <th className="text-end">Savings %</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {recentJobs.map((job, index) => (
                    <tr key={job.job_id || index}>
                      <td>
                        <Badge bg="outline-secondary" text="dark" className="font-monospace">
                          {job.job_id}
                        </Badge>
                      </td>
                      <td className="fw-semibold">{job.model_type}</td>
                      <td>
                        <Badge bg="outline-primary">{job.region}</Badge>
                      </td>
                      <td className="text-end fw-bold">{job.predicted_carbon_kg?.toFixed(2)}</td>
                      <td className="text-end fw-bold text-success">{job.potential_savings_kg?.toFixed(2)}</td>
                      <td className="text-end">
                        <Badge bg="success">{job.savings_percentage?.toFixed(1)}%</Badge>
                      </td>
                      <td>
                        <Badge bg={job.savings_percentage > 20 ? "success" : "warning"}>
                          {job.savings_percentage > 20 ? "High Impact" : "Moderate Impact"}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
              {recentJobs.length === 0 && (
                <div className="text-center py-4 text-muted">
                  No predictions yet. Use the calculator to get started!
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;