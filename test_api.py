#!/usr/bin/env python3
"""Test script to verify the travel agent API end-to-end"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Health check: {response.json()}")
    return response.status_code == 200

def test_create_plan():
    """Test creating a travel plan"""
    print("\n🚀 Testing travel plan creation...")
    print("   This will take 30-60 seconds as AI generates the plan...\n")
    
    data = {
        "user_request": "Plan a 3-day weekend trip to San Francisco with a focus on food and culture, moderate budget",
        "email": "test@example.com"
    }
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{BASE_URL}/plan",
            json=data,
            timeout=120
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Plan created successfully in {elapsed:.1f}s!")
            print(f"\n📊 Response Summary:")
            print(f"   - Success: {result.get('success')}")
            print(f"   - Trip ID: {result.get('trip_id')}")
            print(f"   - Destination: {result.get('plan', {}).get('destination')}")
            
            plan = result.get('plan', {})
            itinerary = plan.get('itinerary', {})
            days = itinerary.get('days', [])
            
            if days:
                print(f"   - Number of days: {len(days)}")
                print(f"\n📅 Sample Day 1:")
                day1 = days[0]
                print(f"      Theme: {day1.get('theme', 'N/A')}")
                if day1.get('morning'):
                    print(f"      Morning: {day1['morning'].get('location', 'N/A')}")
            
            return True, result.get('trip_id')
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"   Error: {response.text}")
            return False, None
            
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out after 120 seconds")
        return False, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None

def main():
    print("="*60)
    print("🧪 TRAVEL AGENT API - END-TO-END TEST")
    print("="*60)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Health check failed. Exiting.")
        return
    
    # Test 2: Create plan
    success, trip_id = test_create_plan()
    
    print("\n" + "="*60)
    if success:
        print("✅ ALL TESTS PASSED!")
        print(f"   Trip ID: {trip_id}")
    else:
        print("❌ TESTS FAILED")
    print("="*60)

if __name__ == "__main__":
    main()
