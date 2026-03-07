import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, Calendar, DollarSign, Sparkles, MessageCircle } from 'lucide-react';
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
            Chat with our AI assistant to plan your perfect trip. Get personalized itineraries with hotels, restaurants, and activities across 19 European destinations.
          </p>
          <button className="btn btn-primary btn-large" onClick={() => navigate('/chat')}>
            <MessageCircle size={20} style={{marginRight: '0.5rem'}} />
            Start Planning Your Trip
          </button>
        </div>
      </header>

      <section className="features">
        <div className="container">
          <h2 className="section-title">How It Works</h2>
          <div className="features-grid">
            <div className="feature-card">
              <MessageCircle className="feature-icon" size={48} />
              <h3>Chat Naturally</h3>
              <p>Describe your trip in plain language — our AI understands your preferences instantly</p>
            </div>
            
            <div className="feature-card">
              <MapPin className="feature-icon" size={48} />
              <h3>Smart Recommendations</h3>
              <p>Get specific hotels, restaurants, and activities pulled from our curated database</p>
            </div>
            
            <div className="feature-card">
              <Calendar className="feature-icon" size={48} />
              <h3>Day-by-Day Itinerary</h3>
              <p>Receive a complete calendar with morning, afternoon, and evening plans</p>
            </div>
            
            <div className="feature-card">
              <DollarSign className="feature-icon" size={48} />
              <h3>Budget Aware</h3>
              <p>Mention your budget and the AI tailors every recommendation to fit it</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <h2>Ready to explore the world?</h2>
          <p>Start planning your next adventure in minutes</p>
          <button className="btn btn-secondary btn-large" onClick={() => navigate('/chat')}>
            Start Chatting
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
