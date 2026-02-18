# Phase 2 Implementation Plan - Interactive Travel Planner

## ✅ Completed
1. Created comprehensive travel database (`data/travel_database.json`)
   - Maldives, Tokyo, Paris with hotels, activities, restaurants
   - Real pricing, ratings, descriptions
   - 30+ options per destination

## 🔄 Next Steps (Priority Order)

### 1. Update Backend RAG System
**File**: `backend/rag/retrieval.py`
- Add fallback to load from `travel_database.json` when Pinecone fails
- Create method `get_destination_data(destination_name)` 
- Return structured data (accommodations, activities, restaurants)

### 2. Enhance Destination Agent  
**File**: `backend/agents/destination_agent.py`
- Use local database instead of RAG embeddings
- Return structured options with IDs for selection
- Include all details: prices, ratings, descriptions

### 3. Create Selection API Endpoints
**File**: `backend/api/routes.py`
Add new endpoints:
- `POST /api/v1/destinations/{destination}/options` - Get all options
- `POST /api/v1/plan/customize` - Save user selections
- `GET /api/v1/plan/{trip_id}/calendar` - Get calendar view

### 4. Enhanced Frontend - Selection Interface
**New File**: `frontend/src/pages/SelectionPage.jsx`
Features:
- **Step 1: Choose Accommodation** (cards with images, prices, amenities)
- **Step 2: Select Activities** (multi-select with time slots)
- **Step 3: Pick Restaurants** (filter by cuisine, price)
- **Step 4: Review & Finalize** (drag-and-drop day planner)

### 5. Calendar/Planner Component
**New File**: `frontend/src/components/TripCalendar.jsx`
Features:
- Day-by-day timeline view
- Drag-and-drop activities to different times
- Add/remove items
- Calculate total cost in real-time
- Export to PDF/iCal buttons

### 6. Enhanced Plan Page Flow
**Update**: `frontend/src/pages/PlanPage.jsx`
New flow:
1. User describes trip → Generate initial plan
2. Show "Customize Your Trip" button
3. Navigate to SelectionPage with options
4. User selects preferences
5. Show TripCalendar for final review
6. Download options (no email required)

## 🎯 User Experience Flow

```
1. Describe Trip
   ↓
2. AI Generates Base Itinerary
   ↓
3. "Customize" Button → Selection Interface
   ↓
4. Browse & Select:
   - Hotels (compare prices/amenities)
   - Activities (see duration/difficulty)
   - Restaurants (filter by cuisine/budget)
   ↓
5. Calendar View
   - Drag-and-drop schedule
   - See timeline & costs
   - Adjust as needed
   ↓
6. Finalize & Download
   - PDF itinerary
   - iCal calendar
   - Budget breakdown
```

## 📊 Example Response Structure

```json
{
  "destination": "Maldives",
  "options": {
    "accommodations": [
      {
        "id": "mald_acc_1",
        "name": "Paradise Island Resort",
        "price_per_night": 300,
        "rating": 4.5,
        "image_url": "...",
        "amenities": ["Pool", "Spa", ...],
        "selected": false
      }
    ],
    "activities": [...],
    "restaurants": [...]
  },
  "user_selections": {
    "accommodation_id": "mald_acc_2",
    "activity_ids": ["mald_act_1", "mald_act_2"],
    "restaurant_ids": ["mald_rest_1", "mald_rest_3"]
  },
  "schedule": {
    "day_1": {
      "morning": "mald_act_1",
      "lunch": "mald_rest_3",
      "afternoon": "Free time",
      "dinner": "mald_rest_1"
    }
  }
}
```

## 🔧 Technical Implementation

### Backend Changes
1. Load JSON database in retrieval.py
2. Create selection storage in database models
3. Add calendar generation logic
4. Enhance PDF export with selected items

### Frontend Changes
1. Create reusable Card components for options
2. Add selection state management
3. Implement calendar drag-and-drop
4. Add filtering/sorting UI
5. Real-time cost calculator

## 🎨 UI Components Needed
- `OptionCard.jsx` - Display hotel/activity/restaurant
- `FilterBar.jsx` - Price range, rating, type filters
- `TripCalendar.jsx` - Day-by-day planner
- `CostSummary.jsx` - Running total display
- `ExportButtons.jsx` - PDF/iCal download

## ⏱️ Estimated Implementation Time
- Backend updates: 1-2 hours
- Frontend selection UI: 2-3 hours
- Calendar component: 1-2 hours
- Testing & polish: 1 hour

**Total**: 5-8 hours of focused development

## 🚀 Quick Win: Start Here
1. Update `retrieval.py` to load JSON (15 min)
2. Update `destination_agent.py` to return structured data (20 min)
3. Test with existing frontend (5 min)
4. User will see rich recommendations immediately!

Then build out the interactive UI progressively.

---

**Ready to implement? Start with the backend changes for immediate results!**
