import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import HomePage from './pages/HomePage';
import PlanPage from './pages/PlanPage';
import SelectionPage from './pages/SelectionPage';
import TripDetailsPage from './pages/TripDetailsPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/plan" element={<PlanPage />} />
          <Route path="/customize" element={<SelectionPage />} />
          <Route path="/trip/:tripId" element={<TripDetailsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
