import React, { useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import WorkloadCreator from './components/WorkloadCreator';
import CarbonCalculator from './components/CarbonCalculator';
import Dashboard from './components/Dashboard';
import Footer from './components/Footer';
import './index.css';

// Background Animation Component
const AnimatedBackground = () => {
  return (
    <div className="background-animation">
      <div className="floating-shapes">
        <div className="shape"></div>
        <div className="shape"></div>
        <div className="shape"></div>
        <div className="shape"></div>
      </div>
      <div className="particles">
        <div className="particle"></div>
        <div className="particle"></div>
        <div className="particle"></div>
        <div className="particle"></div>
        <div className="particle"></div>
      </div>
      <div className="grid-overlay"></div>
    </div>
  );
};

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleNewPrediction = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="App d-flex flex-column min-vh-100">
      <AnimatedBackground />
      <Header />
      
      <main className="flex-grow-1">
        <Hero />
        <WorkloadCreator onWorkloadCreated={handleNewPrediction} />
        <CarbonCalculator onNewPrediction={handleNewPrediction} />
        <Dashboard refreshTrigger={refreshTrigger} />
      </main>

      <Footer />
    </div>
  );
}

export default App;