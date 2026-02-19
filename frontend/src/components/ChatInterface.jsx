import React, { useState, useEffect, useRef } from 'react';
import { Send, Loader } from 'lucide-react';
import './ChatInterface.css';

// Itinerary Table Component
function ItineraryTable({ planData }) {
  const itinerary = planData?.itinerary || {};
  const days = itinerary.days || [];
  const budget = planData?.budget_breakdown || {};

  return (
    <div className="itinerary-container">
      <div className="itinerary-header">
        <h2>🎉 Your {planData.destination} Travel Plan</h2>
        <p className="itinerary-summary">{planData.summary}</p>
        <div className="budget-summary">
          <span>💰 Total Budget: <strong>${budget.total_cost || 'TBD'}</strong></span>
          {budget.daily_average && <span>📊 Daily Average: ${budget.daily_average}</span>}
        </div>
      </div>

      <div className="itinerary-calendar">
        {days.map((day, dayIndex) => (
          <div key={dayIndex} className="day-card">
            <div className="day-header">
              <div className="day-number">Day {dayIndex + 1}</div>
              <div className="day-theme">{day.theme || day.title || 'Exploration'}</div>
            </div>
            
            <div className="activities-timeline">
              {day.activities && day.activities.length > 0 ? (
                day.activities.map((activity, actIndex) => (
                  <div key={actIndex} className="activity-item">
                    <div className="activity-time">
                      <span className="time-badge">
                        {activity.time || activity.timeSlot || 'All Day'}
                      </span>
                    </div>
                    <div className="activity-details">
                      <h4 className="activity-name">
                        {activity.name || activity.activity || 'Activity'}
                      </h4>
                      {activity.description && (
                        <p className="activity-description">{activity.description}</p>
                      )}
                      {activity.location && (
                        <p className="activity-location">📍 {activity.location}</p>
                      )}
                      {activity.cost && (
                        <p className="activity-cost">💵 {activity.cost}</p>
                      )}
                      {activity.duration && (
                        <p className="activity-duration">⏱️ {activity.duration}</p>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                <div className="activity-item">
                  <div className="activity-details">
                    <p className="activity-description">{day.description || 'Free day for exploration'}</p>
                  </div>
                </div>
              )}
            </div>

            {day.meals && (
              <div className="day-meals">
                <strong>🍽️ Meals:</strong> {day.meals}
              </div>
            )}
            {day.accommodation && (
              <div className="day-accommodation">
                <strong>🏨 Stay:</strong> {day.accommodation}
              </div>
            )}
          </div>
        ))}
      </div>

      {planData.destination_data && (
        <div className="customize-section">
          <button 
            className="customize-btn"
            onClick={() => window.location.href = '/customize'}
          >
            🎨 Customize Your Trip
          </button>
        </div>
      )}
    </div>
  );
}

function ChatInterface({ onPlanReady }) {
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isReady, setIsReady] = useState(false);
  const [profile, setProfile] = useState({});
  const [completeness, setCompleteness] = useState(0);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Start conversation on mount
    startConversation();
  }, []);

  const startConversation = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/conversation/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });

      const data = await response.json();
      setConversationId(data.conversation_id);
      
      setMessages([{
        role: 'agent',
        content: data.agent_message,
        question: data.question,
        suggestions: data.suggestions
      }]);
      
      setProfile(data.profile);
      setCompleteness(data.completeness);
      setIsReady(data.is_ready);
    } catch (error) {
      console.error('Error starting conversation:', error);
      setMessages([{
        role: 'agent',
        content: "Hi! 👋 I'm your travel planning assistant. Where would you like to go?"
      }]);
    }
  };

  const sendMessage = async (message) => {
    if (!message.trim() || !conversationId) return;

    // Add user message to UI
    setMessages(prev => [...prev, { role: 'user', content: message }]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/conversation/${conversationId}/message`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        }
      );

      const data = await response.json();
      
      // Add agent response
      setMessages(prev => [...prev, {
        role: 'agent',
        content: data.agent_message,
        question: data.question,
        suggestions: data.suggestions
      }]);
      
      setProfile(data.profile);
      setCompleteness(data.completeness);
      setIsReady(data.is_ready);
      
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'agent',
        content: "Sorry, I encountered an error. Could you try again?"
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(input);
  };

  const handleSuggestionClick = (suggestion) => {
    sendMessage(suggestion);
  };

  const handleGeneratePlan = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/conversation/${conversationId}/finalize`,
        { method: 'POST' }
      );

      const data = await response.json();
      
      if (data.success && data.plan) {
        // Display the plan inline
        setMessages(prev => [...prev, {
          role: 'agent',
          content: '✅ Your personalized travel plan is ready!',
          isPlan: true,
          planData: data.plan
        }]);
        
        setIsReady(false);
      }
    } catch (error) {
      console.error('Error generating plan:', error);
      setMessages(prev => [...prev, {
        role: 'agent',
        content: "Sorry, I encountered an error generating your plan. Please try again."
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Plan Your Trip</h2>
        {completeness > 0 && (
          <div className="progress-indicator">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${completeness}%` }}
              />
            </div>
            <span className="progress-text">{completeness}% complete</span>
          </div>
        )}
      </div>

      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            {msg.isPlan ? (
              <div className="plan-display-inline">
                <ItineraryTable planData={msg.planData} />
              </div>
            ) : (
              <div className="message-bubble">
                <p style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</p>
                
                {msg.suggestions && msg.suggestions.length > 0 && (
                  <div className="suggestions">
                    {msg.suggestions.map((suggestion, idx) => (
                      <button
                        key={idx}
                        className="suggestion-btn"
                        onClick={() => handleSuggestionClick(suggestion)}
                        disabled={loading}
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
        
        {loading && (
          <div className="message agent">
            <div className="message-bubble typing">
              <Loader className="spinner" size={20} />
              <span>Thinking...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {isReady && !loading && (
        <div className="ready-banner">
          <p>✅ I have enough information to create your plan!</p>
          <button 
            className="generate-plan-btn"
            onClick={handleGeneratePlan}
          >
            Generate My Travel Plan
          </button>
        </div>
      )}

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
          className="chat-input"
        />
        <button 
          type="submit" 
          disabled={loading || !input.trim()}
          className="send-btn"
        >
          <Send size={20} />
        </button>
      </form>

      {profile.destination && (
        <div className="info-panel">
          <h4>Trip Details</h4>
          <ul>
            {profile.destination && (
              <li>📍 {Array.isArray(profile.destination) ? profile.destination.join(', ') : profile.destination}</li>
            )}
            {profile.duration && <li>📅 {profile.duration} days</li>}
            {profile.budget && <li>💰 {profile.budget}</li>}
            {profile.interests && Array.isArray(profile.interests) && profile.interests.length > 0 && (
              <li>🎯 {profile.interests.join(', ')}</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}

export default ChatInterface;
