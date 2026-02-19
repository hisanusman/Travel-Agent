import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { travelAPI } from '../services/api';

function TripDetailsPage() {
  const { tripId } = useParams();
  const navigate = useNavigate();
  const [trip, setTrip] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadTrip();
  }, [tripId]);

  const loadTrip = async () => {
    try {
      const data = await travelAPI.getTrip(tripId);
      setTrip(data);
    } catch (err) {
      setError('Failed to load trip details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="main-content">
        <div className="error">{error}</div>
        <button className="btn btn-primary" onClick={() => navigate('/')}>
          Go Home
        </button>
      </div>
    );
  }

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
        <div className="plan-display">
          <div className="plan-header">
            <h1>{trip?.title || 'Trip Details'}</h1>
            <p>Destination: {trip?.destination}</p>
            <p>Status: {trip?.status}</p>
          </div>

          {trip?.itinerary && (
            <div className="card">
              <h2>Itinerary</h2>
              <pre>{JSON.stringify(trip.itinerary, null, 2)}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TripDetailsPage;
