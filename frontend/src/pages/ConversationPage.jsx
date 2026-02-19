import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ChatInterface from '../components/ChatInterface';
import './ConversationPage.css';

function ConversationPage() {
  const navigate = useNavigate();
  const [plan, setPlan] = useState(null);
  const [tripId, setTripId] = useState(null);

  const handlePlanReady = (generatedPlan, generatedTripId) => {
    setPlan(generatedPlan);
    setTripId(generatedTripId);
    
    // Navigate to trip details with the plan
    navigate(`/trip/${generatedTripId}`, { 
      state: { plan: generatedPlan } 
    });
  };

  return (
    <div className="conversation-page">
      <ChatInterface onPlanReady={handlePlanReady} />
    </div>
  );
}

export default ConversationPage;
