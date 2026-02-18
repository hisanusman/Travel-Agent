"""Quick test for Maldives with local database"""
import requests
import json

url = "http://localhost:8000/api/v1/plan"

payload = {
    "user_request": "Plan a 3-day budget trip to Maldives with snorkeling and local food",
    "email": "test@example.com"
}

print("🧪 Testing Maldives trip with LOCAL DATABASE...")
print("⏳ Please wait 30-60 seconds...\n")

try:
    response = requests.post(url, json=payload, timeout=120)
    
    if response.status_code == 200:
        data = response.json()
        plan = data.get('plan', {})
        
        print("✅ SUCCESS!\n")
        print("=" * 60)
        print(f"Destination: {plan.get('destination', {})}")
        print("=" * 60)
        
        # Check if we got rich data
        if 'accommodations' in plan.get('destination_data', {}):
            acc = plan['destination_data']['accommodations']
            print(f"\n🏨 Accommodations Found: {len(acc)}")
            for hotel in acc[:2]:
                print(f"  - {hotel['name']}: ${hotel['price_per_night']}/night ({hotel['rating']}⭐)")
        
        if 'activities' in plan.get('destination_data', {}):
            act = plan['destination_data']['activities']
            print(f"\n🎯 Activities Found: {len(act)}")
            for activity in act[:3]:
                print(f"  - {activity['name']}: ${activity['price']} ({activity['duration_hours']}hrs)")
        
        if 'restaurants' in plan.get('destination_data', {}):
            rest = plan['destination_data']['restaurants']
            print(f"\n🍽️ Restaurants Found: {len(rest)}")
            for restaurant in rest[:2]:
                print(f"  - {restaurant['name']}: ${restaurant['avg_meal_cost']} ({restaurant['cuisine']})")
        
        print("\n" + "=" * 60)
        print("✨ Rich local database working!")
        
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
