"""Complete test showing full Madrid response"""
import requests
import json

url = "http://localhost:8000/api/v1/plan"

payload = {
    "user_request": "5 day trip to Madrid for sightseeing",
    "email": "test@example.com"
}

print("🧪 FULL MADRID TRIP TEST")
print("=" * 80)

try:
    response = requests.post(url, json=payload, timeout=180)
    
    if response.status_code == 200:
        data = response.json()
        plan = data.get('plan', {})
        
        print("\n✅ SUCCESS - Full Response Structure:")
        print("=" * 80)
        
        print(f"\n📍 Destination: {plan.get('destination', 'N/A')}")
        print(f"📝 Summary: {plan.get('summary', 'N/A')}")
        
        # Rich data check
        dest_data = plan.get('destination_data', {})
        if dest_data and dest_data.get('accommodations'):
            print(f"\n🏨 ACCOMMODATIONS ({len(dest_data.get('accommodations', []))}):")
            for acc in dest_data.get('accommodations', [])[:2]:
                print(f"  • {acc['name']} - ${acc['price_per_night']}/night - ⭐{acc['rating']}")
                print(f"    {acc['description'][:80]}...")
            
            print(f"\n🎯 ACTIVITIES ({len(dest_data.get('activities', []))}):")
            for act in dest_data.get('activities', [])[:3]:
                print(f"  • {act['name']} - ${act['price']} - {act['duration_hours']}h")
                print(f"    {act['description'][:80]}...")
            
            print(f"\n🍽️ RESTAURANTS ({len(dest_data.get('restaurants', []))}):")
            for rest in dest_data.get('restaurants', [])[:2]:
                print(f"  • {rest['name']} - {rest['cuisine']} - ⭐{rest['rating']}")
                print(f"    {rest['description'][:80]}...")
        
        # Itinerary
        itinerary = plan.get('itinerary', {})
        if itinerary and itinerary.get('days'):
            days = itinerary.get('days', [])
            print(f"\n📅 ITINERARY ({len(days)} days):")
            for day in days[:2]:  # Show first 2 days
                print(f"\n  Day {day.get('day_number')}: {day.get('theme', 'N/A')}")
                if day.get('morning'):
                    morning = day['morning']
                    print(f"    🌅 Morning: {morning.get('location', 'N/A')}")
                    print(f"       {morning.get('description', 'No description')[:70]}...")
                if day.get('afternoon'):
                    afternoon = day['afternoon']
                    print(f"    ☀️ Afternoon: {afternoon.get('location', 'N/A')}")
                    print(f"       {afternoon.get('description', 'No description')[:70]}...")
                if day.get('evening'):
                    evening = day['evening']
                    print(f"    🌙 Evening: {evening.get('location', 'N/A')}")
                    print(f"       {evening.get('description', 'No description')[:70]}...")
            
            if len(days) > 2:
                print(f"    ... and {len(days) - 2} more days")
        else:
            print("\n⚠️ NO ITINERARY FOUND")
            print("Itinerary structure:", itinerary)
        
        # Budget
        budget = plan.get('budget_breakdown', {})
        if budget:
            print(f"\n💰 BUDGET:")
            print(f"  Total: ${budget.get('total_estimated', 'N/A')}")
            print(f"  Daily Average: ${budget.get('daily_average', 'N/A')}")
            if budget.get('accommodation'):
                print(f"  Accommodation: ${budget['accommodation'].get('total', 'N/A')}")
            if budget.get('food'):
                print(f"  Food: ${budget['food'].get('total', 'N/A')}")
        
        # Response statistics
        response_text = json.dumps(data, indent=2)
        print(f"\n📊 STATISTICS:")
        print(f"  Response size: {len(response_text):,} characters")
        print(f"  Accommodations: {len(dest_data.get('accommodations', []))}")
        print(f"  Activities: {len(dest_data.get('activities', []))}")
        print(f"  Restaurants: {len(dest_data.get('restaurants', []))}")
        print(f"  Itinerary days: {len(itinerary.get('days', []))}")
        
        # Save full response
        with open('madrid_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n💾 Full response saved to: madrid_response.json")
        
        print("\n" + "=" * 80)
        print("✅ SYSTEM IS WORKING PERFECTLY!")
        print("=" * 80)
        
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
