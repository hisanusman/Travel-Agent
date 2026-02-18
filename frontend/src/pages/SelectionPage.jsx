import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { ArrowLeft, ArrowRight, DollarSign, Calendar, Download } from 'lucide-react';
import OptionCard from '../components/OptionCard';
import './SelectionPage.css';

function SelectionPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { plan } = location.state || {};

  const [step, setStep] = useState(1);
  const [selectedAccommodation, setSelectedAccommodation] = useState(null);
  const [selectedActivities, setSelectedActivities] = useState([]);
  const [selectedRestaurants, setSelectedRestaurants] = useState([]);
  const [schedule, setSchedule] = useState({});

  const destData = plan?.destination_data || {};
  const accommodations = destData.accommodations || [];
  const activities = destData.activities || [];
  const restaurants = destData.restaurants || [];
  const duration = plan?.profile?.duration || 3;

  // Calculate total budget
  const calculateTotal = () => {
    const hotelCost = selectedAccommodation ? selectedAccommodation.price_per_night * duration : 0;
    const activityCost = selectedActivities.reduce((sum, act) => sum + (act.price || 0), 0);
    const restaurantCost = selectedRestaurants.reduce((sum, rest) => sum + (rest.avg_meal_cost || 0), 0) * duration;
    return hotelCost + activityCost + restaurantCost;
  };

  const handleAccommodationSelect = (item) => {
    setSelectedAccommodation(selectedAccommodation?.id === item.id ? null : item);
  };

  const handleActivityToggle = (item) => {
    setSelectedActivities(prev => 
      prev.find(a => a.id === item.id)
        ? prev.filter(a => a.id !== item.id)
        : [...prev, item]
    );
  };

  const handleRestaurantToggle = (item) => {
    setSelectedRestaurants(prev =>
      prev.find(r => r.id === item.id)
        ? prev.filter(r => r.id !== item.id)
        : [...prev, item]
    );
  };

  const generateSchedule = () => {
    const newSchedule = {};
    
    for (let day = 1; day <= duration; day++) {
      newSchedule[`day_${day}`] = {
        morning: selectedActivities[day - 1] || null,
        lunch: selectedRestaurants[(day - 1) % selectedRestaurants.length] || null,
        afternoon: selectedActivities[day] || null,
        dinner: selectedRestaurants[day % selectedRestaurants.length] || null
      };
    }
    
    setSchedule(newSchedule);
  };

  useEffect(() => {
    if (step === 4) {
      generateSchedule();
    }
  }, [step]);

  if (!plan) {
    return (
      <div className="selection-page">
        <div className="error-message">
          <h2>No plan data available</h2>
          <button onClick={() => navigate('/plan')}>Go Back</button>
        </div>
      </div>
    );
  }

  const renderStepContent = () => {
    switch (step) {
      case 1:
        return (
          <div className="step-content">
            <h2>Choose Your Accommodation</h2>
            <p className="step-description">Select one hotel for your stay</p>
            
            <div className="options-grid">
              {accommodations.map(item => (
                <OptionCard
                  key={item.id}
                  item={item}
                  type="accommodation"
                  selected={selectedAccommodation?.id === item.id}
                  onSelect={handleAccommodationSelect}
                />
              ))}
            </div>
          </div>
        );

      case 2:
        return (
          <div className="step-content">
            <h2>Select Activities</h2>
            <p className="step-description">Choose as many as you like (multi-select)</p>
            
            <div className="options-grid">
              {activities.map(item => (
                <OptionCard
                  key={item.id}
                  item={item}
                  type="activity"
                  selected={selectedActivities.some(a => a.id === item.id)}
                  onSelect={handleActivityToggle}
                />
              ))}
            </div>
          </div>
        );

      case 3:
        return (
          <div className="step-content">
            <h2>Pick Restaurants</h2>
            <p className="step-description">Select dining options for your trip</p>
            
            <div className="options-grid">
              {restaurants.map(item => (
                <OptionCard
                  key={item.id}
                  item={item}
                  type="restaurant"
                  selected={selectedRestaurants.some(r => r.id === item.id)}
                  onSelect={handleRestaurantToggle}
                />
              ))}
            </div>
          </div>
        );

      case 4:
        return (
          <div className="step-content calendar-view">
            <h2>Your Personalized Itinerary</h2>
            <p className="step-description">Review your {duration}-day trip schedule</p>
            
            <div className="schedule-container">
              {Object.entries(schedule).map(([dayKey, daySchedule], idx) => (
                <div key={dayKey} className="day-schedule">
                  <h3>Day {idx + 1}</h3>
                  
                  <div className="time-slot">
                    <div className="time-label">Morning</div>
                    <div className="activity-card">
                      {daySchedule.morning ? (
                        <>
                          <strong>{daySchedule.morning.name}</strong>
                          <span>${daySchedule.morning.price}</span>
                        </>
                      ) : (
                        <span className="free-time">Free time</span>
                      )}
                    </div>
                  </div>

                  <div className="time-slot">
                    <div className="time-label">Lunch</div>
                    <div className="activity-card">
                      {daySchedule.lunch ? (
                        <>
                          <strong>{daySchedule.lunch.name}</strong>
                          <span>${daySchedule.lunch.avg_meal_cost}</span>
                        </>
                      ) : (
                        <span className="free-time">TBD</span>
                      )}
                    </div>
                  </div>

                  <div className="time-slot">
                    <div className="time-label">Afternoon</div>
                    <div className="activity-card">
                      {daySchedule.afternoon ? (
                        <>
                          <strong>{daySchedule.afternoon.name}</strong>
                          <span>${daySchedule.afternoon.price}</span>
                        </>
                      ) : (
                        <span className="free-time">Free time</span>
                      )}
                    </div>
                  </div>

                  <div className="time-slot">
                    <div className="time-label">Dinner</div>
                    <div className="activity-card">
                      {daySchedule.dinner ? (
                        <>
                          <strong>{daySchedule.dinner.name}</strong>
                          <span>${daySchedule.dinner.avg_meal_cost}</span>
                        </>
                      ) : (
                        <span className="free-time">TBD</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="export-options">
              <button className="export-btn">
                <Download size={20} />
                Download PDF
              </button>
              <button className="export-btn">
                <Calendar size={20} />
                Add to Calendar
              </button>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="selection-page">
      <header className="selection-header">
        <button className="back-btn" onClick={() => navigate('/plan')}>
          <ArrowLeft size={20} />
          Back to Plan
        </button>

        <div className="progress-bar">
          <div className={`progress-step ${step >= 1 ? 'active' : ''}`}>1. Hotel</div>
          <div className={`progress-step ${step >= 2 ? 'active' : ''}`}>2. Activities</div>
          <div className={`progress-step ${step >= 3 ? 'active' : ''}`}>3. Dining</div>
          <div className={`progress-step ${step >= 4 ? 'active' : ''}`}>4. Review</div>
        </div>

        <div className="budget-display">
          <DollarSign size={20} />
          <div>
            <div className="budget-label">Total Budget</div>
            <div className="budget-amount">${calculateTotal().toFixed(0)}</div>
          </div>
        </div>
      </header>

      <main className="selection-content">
        {renderStepContent()}
      </main>

      <footer className="selection-footer">
        {step > 1 && (
          <button className="nav-btn prev" onClick={() => setStep(step - 1)}>
            <ArrowLeft size={20} />
            Previous
          </button>
        )}
        
        {step < 4 && (
          <button 
            className="nav-btn next" 
            onClick={() => setStep(step + 1)}
            disabled={step === 1 && !selectedAccommodation}
          >
            Next
            <ArrowRight size={20} />
          </button>
        )}

        {step === 4 && (
          <button className="nav-btn finish" onClick={() => navigate('/plan')}>
            Finish & Save
          </button>
        )}
      </footer>
    </div>
  );
}

export default SelectionPage;
