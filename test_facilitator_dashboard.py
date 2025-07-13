#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5000"

def test_facilitator_dashboard_routes():
    """Test facilitator dashboard routes"""
    print("Testing facilitator dashboard routes...")
    
    # Test the dashboard page route
    print("\n1. Testing dashboard page route...")
    try:
        response = requests.get(f"{BASE_URL}/api/facilitator/dashboard-page")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Dashboard page route working")
            print(f"   Content length: {len(response.text)} characters")
            if "Facilitator Dashboard" in response.text:
                print("   ✅ HTML content contains 'Facilitator Dashboard'")
            else:
                print("   ❌ HTML content doesn't contain expected title")
        else:
            print("   ❌ Dashboard page route failed")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error testing dashboard page: {e}")
    
    # Test the dashboard HTML route
    print("\n2. Testing dashboard HTML route...")
    try:
        response = requests.get(f"{BASE_URL}/api/facilitator/dashboard.html")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Dashboard HTML route working")
            print(f"   Content length: {len(response.text)} characters")
        else:
            print("   ❌ Dashboard HTML route failed")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error testing dashboard HTML: {e}")
    
    # Test the dashboard API route (should require authentication)
    print("\n3. Testing dashboard API route (no auth)...")
    try:
        response = requests.get(f"{BASE_URL}/api/facilitator/dashboard")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Dashboard API route correctly requires authentication")
        else:
            print("   ❌ Dashboard API route should require authentication")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error testing dashboard API: {e}")

if __name__ == "__main__":
    test_facilitator_dashboard_routes() 