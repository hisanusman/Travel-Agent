import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, Calendar, DollarSign, Sparkles } from 'lucide-react';
import './HomePage.css';

function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="home-page">
      <header className="hero">
        <div className="hero-content">
          <h1 className="hero-title">
            <Sparkles className="icon-inline" />
            AI-Powered Travel Planning
          </h1>
          <p className="hero-subtitle">
            Tell us your dream destination, and let our intelligent agents create the perfect itinerary for you
          </p>
          <button className="btn btn-primary btn-large" onClick={() => navigate('/plan')}>
            Start Planning Your Trip
          </button>
        </div>
      </header>

      <section className="features">
        <div className="container">
          <h2 className="section-title">How It Works</h2>
          <div className="features-grid">
            <div className="feature-card">
              <MapPin className="feature-icon" size={48} />
              <h3>Describe Your Trip</h3>
              <p>Simply tell us where you want to go, your interests, and travel style</p>
            </div>
            
            <div className="feature-card">
              <Calendar className="feature-icon" size={48} />
              <h3>Get Custom Itinerary</h3>
              <p>Our AI agents create a personalized day-by-day plan optimized for you</p>
            </div>
            
            <div className="feature-card">
              <DollarSign className="feature-icon" size={48} />
              <h3>Budget Planning</h3>
              <p>Receive detailed cost breakdowns and budget-friendly recommendations</p>
            </div>
            
            <div className="feature-card">
              <Sparkles className="feature-icon" size={48} />
              <h3>Smart Optimization</h3>
              <p>Weather-aware planning, optimized routes, and personalized suggestions</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <h2>Ready to explore the world?</h2>
          <p>Start planning your next adventure in minutes</p>
          <button className="btn btn-secondary btn-large" onClick={() => navigate('/plan')}>
            Create Your Itinerary
          </button>
        </div>
      </section>

      <footer className="footer">
        <div className="container">
          <p>&copy; 2026 Travel Agent. Powered by AI.</p>
        </div>
      </footer>
    </div>
  );
}

export default HomePage;
