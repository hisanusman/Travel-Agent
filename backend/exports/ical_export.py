"""
iCal Export - Generate calendar files for itineraries
"""

from typing import Dict, Any
from icalendar import Calendar, Event, vText
from datetime import datetime, timedelta
from backend.config import settings
from loguru import logger
import pytz

class ICalExporter:
    """Export travel itineraries to iCal format"""
    
    def __init__(self):
        self.timezone = pytz.UTC
    
    def export_itinerary(self, travel_plan: Dict[str, Any], filename: str = None) -> str:
        """
        Export travel plan to iCal format
        
        Args:
            travel_plan: Complete travel plan dictionary
            filename: Optional custom filename
            
        Returns:
            Path to generated iCal file
        """
        try:
            plan = travel_plan.get('plan', {})
            profile = plan.get('profile', {})
            destination = plan.get('destination', 'Trip')
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"itinerary_{destination}_{timestamp}.ics"
            
            # Ensure exports directory exists
            output_path = settings.EXPORTS_DIR / filename
            
            # Create calendar
            cal = Calendar()
            cal.add('prodid', '-//Travel Agent//Itinerary//EN')
            cal.add('version', '2.0')
            cal.add('calscale', 'GREGORIAN')
            cal.add('method', 'PUBLISH')
            cal.add('x-wr-calname', f'Travel to {destination}')
            cal.add('x-wr-timezone', 'UTC')
            cal.add('x-wr-caldesc', f"Itinerary for trip to {destination}")
            
            # Parse start date
            start_date_str = profile.get('dates', '')
            try:
                # Try to parse date - simplified for now
                base_date = datetime.now() + timedelta(days=30)  # Default to 30 days from now
            except:
                base_date = datetime.now() + timedelta(days=30)
            
            # Add events for each day's activities
            itinerary = plan.get('itinerary', {})
            days = itinerary.get('days', [])
            
            for i, day in enumerate(days):
                current_date = base_date + timedelta(days=i)
                day_number = day.get('day_number', i + 1)
                theme = day.get('theme', 'Travel Day')
                
                # Morning activity
                morning = day.get('morning', {})
                if morning and isinstance(morning, dict):
                    self._add_activity_event(
                        cal, morning, current_date, 9, 0, destination, f"Day {day_number}"
                    )
                
                # Afternoon activity
                afternoon = day.get('afternoon', {})
                if afternoon and isinstance(afternoon, dict):
                    self._add_activity_event(
                        cal, afternoon, current_date, 14, 0, destination, f"Day {day_number}"
                    )
                
                # Evening activity
                evening = day.get('evening', {})
                if evening and isinstance(evening, dict):
                    self._add_activity_event(
                        cal, evening, current_date, 19, 0, destination, f"Day {day_number}"
                    )
            
            # Write to file
            with open(output_path, 'wb') as f:
                f.write(cal.to_ical())
            
            logger.info(f"iCal exported successfully: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error exporting iCal: {e}")
            raise
    
    def _add_activity_event(
        self,
        cal: Calendar,
        activity: Dict[str, Any],
        date: datetime,
        hour: int,
        minute: int,
        destination: str,
        day_label: str
    ):
        """Add a single activity as a calendar event"""
        try:
            event = Event()
            
            # Set event time
            start_time = datetime(
                date.year, date.month, date.day,
                hour, minute,
                tzinfo=self.timezone
            )
            
            # Duration (default 2 hours)
            duration_hours = activity.get('duration', 2)
            if isinstance(duration_hours, str):
                # Parse duration string if needed
                duration_hours = 2
            end_time = start_time + timedelta(hours=duration_hours)
            
            # Event details
            location = activity.get('location', 'TBD')
            description = activity.get('description', '')
            
            event.add('summary', f"{location} - {destination}")
            event.add('dtstart', start_time)
            event.add('dtend', end_time)
            event.add('dtstamp', datetime.now(self.timezone))
            event.add('location', vText(location))
            event.add('description', vText(f"{day_label}\n\n{description}"))
            
            # Add cost if available
            cost = activity.get('cost', '')
            if cost:
                event.add('description', vText(f"{description}\n\nEstimated cost: ${cost}"))
            
            cal.add_component(event)
            
        except Exception as e:
            logger.warning(f"Could not add activity event: {e}")

# Global exporter instance
ical_exporter = ICalExporter()
