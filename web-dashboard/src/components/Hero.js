import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { Zap, Leaf, Cloud } from 'lucide-react';

const Hero = () => {
  const handleStartOptimizing = () => {
    const workloadElement = document.getElementById('workload-creator');
    if (workloadElement) {
      workloadElement.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="hero-bg py-5">
      <Container className="my-5 py-5">
        <Row className="align-items-center">
          <Col lg={6}>
            <div className="mb-4">
              <h1 className="display-4 fw-bold text-dark mb-4">
                Optimize Cloud Resources,{' '}
                <span className="text-gradient">Minimize Carbon Footprint</span>
              </h1>
              <p className="lead text-muted mb-4 fs-5">
                AI-powered platform that intelligently allocates cloud resources for your ML workloads 
                while tracking and reducing carbon emissions through blockchain-verified credits.
              </p>
            </div>
            
            <div className="d-flex gap-3 mb-5">
              <Button 
                variant="success" 
                size="lg" 
                className="px-4 py-3 fw-semibold pulse-glow"
                onClick={handleStartOptimizing}
              >
                <Zap size={20} className="me-2" />
                Start Optimizing
              </Button>
              <Button 
                variant="outline-success" 
                size="lg" 
                className="px-4 py-3 fw-semibold border-gradient"
                onClick={() => document.getElementById('calculator').scrollIntoView({ behavior: 'smooth' })}
              >
                Calculate Carbon
              </Button>
            </div>

            {/* Stats with floating animation */}
            <Row className="g-4">
              <Col xs={4}>
                <div className="text-center float-animation">
                  <div className="text-success fw-bold fs-3">30%+</div>
                  <small className="text-muted">Carbon Reduction</small>
                </div>
              </Col>
              <Col xs={4}>
                <div className="text-center float-animation" style={{animationDelay: '2s'}}>
                  <div className="text-success fw-bold fs-3">50+</div>
                  <small className="text-muted">Workloads Optimized</small>
                </div>
              </Col>
              <Col xs={4}>
                <div className="text-center float-animation" style={{animationDelay: '4s'}}>
                  <div className="text-success fw-bold fs-3">100%</div>
                  <small className="text-muted">Blockchain Verified</small>
                </div>
              </Col>
            </Row>
          </Col>
          
          <Col lg={6}>
            <div className="position-relative">
              <div className="bg-success bg-opacity-10 rounded-3 p-5 card-hover">
                <div className="d-flex justify-content-center mb-4">
                  <div className="bg-success rounded-circle p-4 float-animation">
                    <Cloud size={48} className="text-white" />
                  </div>
                </div>
                <h4 className="text-center fw-bold mb-3">AI-Powered Optimization</h4>
                <p className="text-center text-muted mb-0">
                  Our ML engine analyzes your workload requirements and automatically selects 
                  the most efficient cloud configuration to minimize costs and carbon emissions.
                </p>
              </div>
              
              {/* Floating elements */}
              <div className="position-absolute top-0 start-0 mt-3 ms-3 float-animation">
                <div className="bg-warning rounded-circle p-2">
                  <Leaf size={20} className="text-white" />
                </div>
              </div>
              <div className="position-absolute bottom-0 end-0 mb-3 me-3 float-animation" style={{animationDelay: '3s'}}>
                <div className="bg-info rounded-circle p-2">
                  <Zap size={20} className="text-white" />
                </div>
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Hero;