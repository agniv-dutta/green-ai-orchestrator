import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { Heart, Github, Zap } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="footer text-white mt-5 py-4">
      <Container>
        <Row className="align-items-center">
          <Col md={6}>
            <div className="d-flex align-items-center">
              <Zap size={20} className="me-2 text-warning" />
              <span>
                Made with <Heart size={16} className="text-danger mx-1" /> 
                for a greener AI future
              </span>
            </div>
          </Col>
          <Col md={6} className="text-md-end">
            <div className="d-flex align-items-center justify-content-md-end">
              <span className="me-3">GreenML Optimizer v1.0</span>
              <a 
                href="#github" 
                className="text-white text-decoration-none d-flex align-items-center"
              >
                <Github size={16} className="me-1" />
                Source
              </a>
            </div>
            <small className="text-muted">
              Reduce your ML carbon footprint by 30%+ through intelligent scheduling
            </small>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;