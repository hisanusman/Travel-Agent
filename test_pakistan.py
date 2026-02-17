#!/usr/bin/env python3
"""Test API with Pakistan destination"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_pakistan_trip():
    print("🧪 Testing travel plan for Pakistan...")
    print("⏳ This may take 30-60 seconds for AI to generate...\n")
    
    data = {
        "user_request": "Plan a 5-day cultural trip to Pakistan visiting Lahore and Islamabad, moderate budget",
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/plan",
            json=data,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Plan created for Pakistan!\n")
            print(f"Destination: {result.get('plan', {}).get('destination')}")
            
            # Show first day
            plan = result.get('plan', {})
            itinerary = plan.get('itinerary', {})
            days = itinerary.get('days', [])
            
            if days:
                print(f"\nDay 1 Preview:")
                day1 = days[0]
                print(f"  Theme: {day1.get('theme', 'N/A')}")
                if day1.get('morning'):
                    morning = day1['morning']
                    loc = morning.get('location', 'N/A') if isinstance(morning, dict) else morning
                    print(f"  Morning: {loc}")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_pakistan_trip()
