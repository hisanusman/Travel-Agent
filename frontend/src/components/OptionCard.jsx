import React from 'react';
import { Check, Star, MapPin } from 'lucide-react';
import './OptionCard.css';

function OptionCard({ 
  item, 
  type, 
  selected, 
  onSelect,
  showSelectButton = true 
}) {
  const renderPrice = () => {
    if (type === 'accommodation') {
      return `$${item.price_per_night}/night`;
    } else if (type === 'activity') {
      return `$${item.price}`;
    } else if (type === 'restaurant') {
      return `$${item.avg_meal_cost}/meal`;
    }
  };

  const renderDuration = () => {
    if (type === 'activity' && item.duration_hours) {
      return `${item.duration_hours} hours`;
    }
    return null;
  };

  const renderRating = () => {
    if (item.rating) {
      return (
        <div className="rating">
          <Star size={16} fill="#FFD700" color="#FFD700" />
          <span>{item.rating}</span>
        </div>
      );
    }
    return null;
  };

  return (
    <div className={`option-card ${selected ? 'selected' : ''}`}>
      {selected && (
        <div className="selected-badge">
          <Check size={16} />
          Selected
        </div>
      )}
      
      <div className="card-header">
        <h3>{item.name}</h3>
        {renderRating()}
      </div>

      {item.location && (
        <div className="location">
          <MapPin size={14} />
          <span>{item.location}</span>
        </div>
      )}

      <p className="description">{item.description}</p>

      <div className="card-details">
        <div className="price">{renderPrice()}</div>
        {renderDuration() && <div className="duration">{renderDuration()}</div>}
        {item.difficulty && <div className="difficulty">{item.difficulty}</div>}
        {item.cuisine && <div className="cuisine">{item.cuisine}</div>}
      </div>

      {item.amenities && (
        <div className="amenities">
          {item.amenities.slice(0, 4).map((amenity, idx) => (
            <span key={idx} className="amenity-tag">{amenity}</span>
          ))}
        </div>
      )}

      {item.specialties && (
        <div className="specialties">
          <strong>Specialties:</strong> {item.specialties.slice(0, 2).join(', ')}
        </div>
      )}

      {showSelectButton && (
        <button 
          className={`select-btn ${selected ? 'selected' : ''}`}
          onClick={() => onSelect(item)}
        >
          {selected ? 'Selected ✓' : 'Select'}
        </button>
      )}
    </div>
  );
}

export default OptionCard;
