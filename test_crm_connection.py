#!/usr/bin/env python3
"""
Simple test script to check if CRM service is working
"""

import requests
import json

def test_crm_service():
    """Test if CRM service is responding"""
    base_url = "http://localhost:5001"
    
    print("Testing CRM Service Connection")
    print("=" * 40)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed: {data.get('status')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: Notifications endpoint
    print("2. Testing notifications endpoint...")
    try:
        response = requests.get(f"{base_url}/notifications", timeout=5)
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            print(f"   ✅ Notifications endpoint working: {count} notifications found")
        else:
            print(f"   ❌ Notifications endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Notifications endpoint error: {e}")
        return False
    
    # Test 3: Dashboard endpoint
    print("3. Testing dashboard endpoint...")
    try:
        response = requests.get(f"{base_url}/dashboard", timeout=5)
        if response.status_code == 200:
            print("   ✅ Dashboard endpoint working")
        else:
            print(f"   ❌ Dashboard endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Dashboard endpoint error: {e}")
        return False
    
    print("\n🎉 All tests passed! CRM service is working correctly.")
    print("\nYou can now:")
    print("   - View notifications at: http://localhost:5001/dashboard")
    print("   - Check API at: http://localhost:5001/notifications")
    print("   - Health check at: http://localhost:5001/health")
    
    return True

if __name__ == "__main__":
    test_crm_service() 