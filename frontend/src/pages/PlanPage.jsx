import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Loader, ArrowLeft } from 'lucide-react';
import { travelAPI } from '../services/api';
import './PlanPage.css';

function PlanPage() {
  const navigate = useNavigate();
  const [userRequest, setUserRequest] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [plan, setPlan] = useState(null);
  const [tripId, setTripId] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!userRequest.trim()) {
      setError('Please describe your trip');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await travelAPI.createPlan(userRequest, email || null);
      
      if (response.success) {
        setPlan(response.plan);
        setTripId(response.trip_id);
        
        // Check if we have rich destination data for customization
        const hasRichData = response.plan?.destination_data?.accommodations?.length > 0;
        console.log('Has rich data:', hasRichData, response.plan?.destination_data);
        
      } else {
        setError('Failed to create travel plan');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while creating your plan');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const examplePrompts = [
    "Plan a 7-day cultural trip to Japan in autumn on a moderate budget",
    "Weekend getaway to Paris for couples on a luxury budget",
    "10-day adventure trip to New Zealand for hiking and nature",
    "5-day family-friendly beach vacation in Hawaii"
  ];

  return (
    <div className="plan-page">
      <header className="header">
        <div className="header-content">
          <button className="btn-back" onClick={() => navigate('/')}>
            <ArrowLeft size={20} />
            Back to Home
          </button>
        </div>
      </header>

      <div className="main-content">
        {!plan ? (
          <div className="plan-form-container">
            <h1 className="page-title">Describe Your Dream Trip</h1>
            <p className="page-subtitle">
              Tell us where you want to go, your interests, budget, and travel style
            </p>

            <form onSubmit={handleSubmit} className="plan-form">
              <div className="form-group">
                <label htmlFor="userRequest">What kind of trip are you planning?</label>
                <textarea
                  id="userRequest"
                  value={userRequest}
                  onChange={(e) => setUserRequest(e.target.value)}
                  placeholder="Example: Plan a 7-day cultural trip to Japan in autumn on a moderate budget. I'm interested in traditional temples, local cuisine, and historical sites."
                  rows={6}
                  className="form-textarea"
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">Email (optional - to save your itinerary)</label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="your@email.com"
                  className="form-input"
                  disabled={loading}
                />
              </div>

              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? (
                  <>
                    <Loader className="spinning" size={20} />
                    Creating Your Plan...
                  </>
                ) : (
                  <>
                    <Send size={20} />
                    Generate Itinerary
                  </>
                )}
              </button>
            </form>

            <div className="examples">
              <h3>Try these examples:</h3>
              <div className="example-chips">
                {examplePrompts.map((prompt, index) => (
                  <button
                    key={index}
                    className="example-chip"
                    onClick={() => setUserRequest(prompt)}
                    disabled={loading}
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>

            {error && (
              <div className="error">
                <strong>Error:</strong> {error}
              </div>
            )}
          </div>
        ) : (
          <TravelPlanDisplay plan={plan} tripId={tripId} />
        )}
      </div>
    </div>
  );
}

function TravelPlanDisplay({ plan, tripId }) {
  const navigate = useNavigate();
  const [exporting, setExporting] = useState(false);

  const handleExport = async (format) => {
    if (!tripId) {
      alert('Please provide an email to export your itinerary');
      return;
    }

    setExporting(true);
    try {
      const response = await travelAPI.exportItinerary(tripId, format);
      if (response.success) {
        alert(`Exported as ${format}! File: ${response.file_path}`);
      }
    } catch (err) {
      alert('Failed to export itinerary');
      console.error(err);
    } finally {
      setExporting(false);
    }
  };

  // Check if we have rich destination data for customization
  const hasRichData = plan?.destination_data?.accommodations?.length > 0;

  return (
    <div className="plan-display">
      <div className="plan-header">
        <div className="header-content">
          <h1>Your Travel Plan to {plan.destination}</h1>
          {hasRichData && (
            <button 
              className="customize-btn"
              onClick={() => navigate('/customize', { state: { plan } })}
            >
              🎨 Customize Your Trip
            </button>
          )}
        </div>
        <p className="plan-summary">{plan.summary}</p>
      </div>

      {plan.budget_breakdown && (
        <div className="card">
          <h2>Budget Overview</h2>
          <div className="budget-summary">
            <div className="budget-item">
              <span>Total Estimated Cost:</span>
              <strong>${plan.budget_breakdown.total_estimated || 'N/A'}</strong>
            </div>
            <div className="budget-item">
              <span>Daily Average:</span>
              <strong>${plan.budget_breakdown.daily_average || 'N/A'}</strong>
            </div>
          </div>
        </div>
      )}

      {plan.itinerary && plan.itinerary.days && (
        <div className="card">
          <h2>Day-by-Day Itinerary</h2>
          {plan.itinerary.days.map((day, index) => (
            <div key={index} className="day-card">
              <h3>Day {day.day_number}: {day.theme}</h3>
              
              {day.morning && (
                <div className="activity">
                  <h4>🌅 Morning</h4>
                  <p><strong>{day.morning.location || 'Activity'}</strong></p>
                  {day.morning.description && <p>{day.morning.description}</p>}
                  {day.morning.time && <p className="time">⏰ {day.morning.time}</p>}
                </div>
              )}

              {day.afternoon && (
                <div className="activity">
                  <h4>☀️ Afternoon</h4>
                  <p><strong>{day.afternoon.location || 'Activity'}</strong></p>
                  {day.afternoon.description && <p>{day.afternoon.description}</p>}
                  {day.afternoon.time && <p className="time">⏰ {day.afternoon.time}</p>}
                </div>
              )}

              {day.evening && (
                <div className="activity">
                  <h4>🌙 Evening</h4>
                  <p><strong>{day.evening.location || 'Activity'}</strong></p>
                  {day.evening.description && <p>{day.evening.description}</p>}
                  {day.evening.time && <p className="time">⏰ {day.evening.time}</p>}
                </div>
              )}

              {day.notes && (
                <div className="day-notes">
                  <em>{day.notes}</em>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="export-actions">
        <h3>Export Your Itinerary</h3>
        <div className="export-buttons">
          <button 
            className="btn btn-secondary" 
            onClick={() => handleExport('pdf')}
            disabled={exporting || !tripId}
          >
            📄 Download PDF
          </button>
          <button 
            className="btn btn-secondary" 
            onClick={() => handleExport('ical')}
            disabled={exporting || !tripId}
          >
            📅 Add to Calendar
          </button>
          <button 
            className="btn btn-secondary" 
            onClick={() => handleExport('map')}
            disabled={exporting || !tripId}
          >
            🗺️ View on Map
          </button>
        </div>
      </div>

      <button className="btn btn-primary" onClick={() => window.location.reload()}>
        Plan Another Trip
      </button>
    </div>
  );
}

export default PlanPage;
