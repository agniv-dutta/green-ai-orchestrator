import React from 'react';
import { Navbar, Container, Nav, Badge } from 'react-bootstrap';
import { Leaf, Zap, Brain } from 'lucide-react';

const Header = () => {
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <Navbar bg="white" variant="light" expand="lg" className="shadow-sm" fixed="top">
      <Container>
        <Navbar.Brand 
          href="#home" 
          className="d-flex align-items-center text-success"
          onClick={(e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }}
          style={{ cursor: 'pointer' }}
        >
          <Brain size={32} className="me-2" />
          <div>
            <h4 className="mb-0 fw-bold">GreenML Optimizer</h4>
            <small className="opacity-75">AI-Powered Carbon Calculator</small>
          </div>
        </Navbar.Brand>
        
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link 
              href="#workload-creator" 
              className="fw-semibold text-dark"
              onClick={(e) => {
                e.preventDefault();
                scrollToSection('workload-creator');
              }}
            >
              Create Workload
            </Nav.Link>
            <Nav.Link 
              href="#calculator" 
              className="fw-semibold text-dark"
              onClick={(e) => {
                e.preventDefault();
                scrollToSection('calculator');
              }}
            >
              Calculator
            </Nav.Link>
            <Nav.Link 
              href="#dashboard" 
              className="fw-semibold text-dark"
              onClick={(e) => {
                e.preventDefault();
                scrollToSection('dashboard');
              }}
            >
              Dashboard
            </Nav.Link>
            <Badge bg="success" className="ms-2 d-flex align-items-center">
              <Zap size={16} className="me-1" />
              Save 30%+ Carbon
            </Badge>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;