import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3303/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const travelAPI = {
  // Create a new travel plan
  createPlan: async (userRequest, email = null) => {
    const response = await api.post('/plan', {
      user_request: userRequest,
      email: email,
    });
    return response.data;
  },

  // Update an existing travel plan
  updatePlan: async (tripId, updateRequest) => {
    const response = await api.put('/plan/update', {
      trip_id: tripId,
      update_request: updateRequest,
    });
    return response.data;
  },

  // Export itinerary
  exportItinerary: async (tripId, format) => {
    const response = await api.post('/export', {
      trip_id: tripId,
      format: format,
    });
    return response.data;
  },

  // Get user trips
  getUserTrips: async (userId) => {
    const response = await api.get(`/users/${userId}/trips`);
    return response.data;
  },

  // Get specific trip
  getTrip: async (tripId) => {
    const response = await api.get(`/trips/${tripId}`);
    return response.data;
  },

  // Delete trip
  deleteTrip: async (tripId) => {
    const response = await api.delete(`/trips/${tripId}`);
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
