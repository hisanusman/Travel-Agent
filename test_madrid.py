"""Test Madrid trip"""
import requests
import json

url = "http://localhost:8000/api/v1/plan"

payload = {
    "user_request": "5 day trip to Madrid for sightseeing",
    "email": "test@example.com"
}

print("🧪 Testing Madrid trip...")
print("=" * 60)

try:
    response = requests.post(url, json=payload, timeout=180)
    
    if response.status_code == 200:
        data = response.json()
        plan = data.get('plan', {})
        
        print("✅ SUCCESS!")
        print("=" * 60)
        print(f"\n📍 Destination: {plan.get('destination', 'N/A')}")
        print(f"\n📝 Summary: {plan.get('summary', 'N/A')}")
        
        # Check destination data
        dest_data = plan.get('destination_data', {})
        if dest_data:
            print(f"\n🏨 Accommodations: {len(dest_data.get('accommodations', []))}")
            print(f"🎯 Activities: {len(dest_data.get('activities', []))}")
            print(f"🍽️ Restaurants: {len(dest_data.get('restaurants', []))}")
        else:
            print("\n⚠️ NO RICH DATA - Using AI fallback")
        
        # Check itinerary
        itinerary = plan.get('itinerary', {})
        if itinerary:
            days = itinerary.get('days', [])
            print(f"\n📅 Itinerary Days: {len(days)}")
            if days:
                print(f"\nDay 1 Preview:")
                day1 = days[0]
                print(f"  Theme: {day1.get('theme', 'N/A')}")
                print(f"  Morning: {day1.get('morning', {}).get('location', 'N/A')}")
        else:
            print("\n⚠️ NO ITINERARY GENERATED")
        
        # Check budget
        budget = plan.get('budget_breakdown', {})
        if budget:
            print(f"\n💰 Budget: ${budget.get('total_estimated', 'N/A')}")
        
        # Full response size check
        response_text = json.dumps(data, indent=2)
        print(f"\n📊 Response size: {len(response_text)} characters")
        
        if len(response_text) < 500:
            print("\n❌ RESPONSE TOO SHORT!")
            print("Full response:")
            print(response_text)
        else:
            print("\n✅ Response has good detail")
        
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
