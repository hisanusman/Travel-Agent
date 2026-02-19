"""
Map Export - Generate interactive maps for itineraries
"""

from typing import Dict, Any, List, Tuple
import folium
from folium import plugins
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from backend.config import settings
from loguru import logger
import time

class MapExporter:
    """Generate interactive maps showing itinerary locations"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="travel-agent-app")
        self.cache = {}  # Simple cache for geocoded locations
    
    def export_map(self, travel_plan: Dict[str, Any], filename: str = None) -> str:
        """
        Export travel plan as an interactive map
        
        Args:
            travel_plan: Complete travel plan dictionary
            filename: Optional custom filename
            
        Returns:
            Path to generated HTML map file
        """
        try:
            plan = travel_plan.get('plan', {})
            destination = plan.get('destination', 'Trip')
            
            # Generate filename if not provided
            if not filename:
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"map_{destination}_{timestamp}.html"
            
            # Ensure exports directory exists
            output_path = settings.EXPORTS_DIR / filename
            
            # Get center coordinates for destination
            center_coords = self._geocode_location(destination)
            
            # Create map
            travel_map = folium.Map(
                location=center_coords,
                zoom_start=12,
                tiles='OpenStreetMap'
            )
            
            # Collect all locations from itinerary
            locations = self._extract_locations(plan)
            
            # Add markers for each location
            colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred']
            
            for i, (day, location_name, activity_info) in enumerate(locations):
                coords = self._geocode_location(f"{location_name}, {destination}")
                
                if coords:
                    color = colors[day % len(colors)]
                    
                    # Create popup content
                    popup_html = f"""
                    <div style="font-family: Arial; width: 200px;">
                        <h4 style="margin: 0; color: #{color};">Day {day}</h4>
                        <p style="margin: 5px 0;"><b>{location_name}</b></p>
                        <p style="margin: 5px 0; font-size: 12px;">{activity_info}</p>
                    </div>
                    """
                    
                    # Add marker
                    folium.Marker(
                        location=coords,
                        popup=folium.Popup(popup_html, max_width=250),
                        tooltip=f"Day {day}: {location_name}",
                        icon=folium.Icon(color=color, icon='info-sign')
                    ).add_to(travel_map)
            
            # Add minimap
            minimap = plugins.MiniMap(toggle_display=True)
            travel_map.add_child(minimap)
            
            # Add fullscreen button
            plugins.Fullscreen(
                position='topright',
                title='Fullscreen',
                title_cancel='Exit fullscreen',
                force_separate_button=True
            ).add_to(travel_map)
            
            # Save map
            travel_map.save(str(output_path))
            
            logger.info(f"Map exported successfully: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error exporting map: {e}")
            raise
    
    def _geocode_location(self, location: str) -> Tuple[float, float]:
        """
        Get coordinates for a location
        
        Returns:
            Tuple of (latitude, longitude)
        """
        # Check cache first
        if location in self.cache:
            return self.cache[location]
        
        try:
            time.sleep(1)  # Rate limiting
            geo_location = self.geolocator.geocode(location)
            
            if geo_location:
                coords = (geo_location.latitude, geo_location.longitude)
                self.cache[location] = coords
                return coords
            else:
                logger.warning(f"Could not geocode location: {location}")
                return (0, 0)
                
        except GeocoderTimedOut:
            logger.warning(f"Geocoding timeout for: {location}")
            return (0, 0)
        except Exception as e:
            logger.error(f"Geocoding error for {location}: {e}")
            return (0, 0)
    
    def _extract_locations(self, plan: Dict[str, Any]) -> List[Tuple[int, str, str]]:
        """
        Extract all locations from itinerary
        
        Returns:
            List of tuples (day_number, location_name, activity_info)
        """
        locations = []
        itinerary = plan.get('itinerary', {})
        days = itinerary.get('days', [])
        
        for day in days:
            day_number = day.get('day_number', 1)
            
            # Extract activities from each period
            for period in ['morning', 'afternoon', 'evening']:
                activity = day.get(period, {})
                if isinstance(activity, dict):
                    location = activity.get('location', '')
                    description = activity.get('description', '')
                    time = activity.get('time', '')
                    
                    if location:
                        info = f"{period.capitalize()} ({time}): {description[:100]}"
                        locations.append((day_number, location, info))
        
        return locations

# Global exporter instance
map_exporter = MapExporter()
