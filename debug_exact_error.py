#!/usr/bin/env python3
"""
Debug exact error from Flask server
"""

import os
import requests
import json

def test_with_detailed_error():
    """Test registration and show detailed error"""
    
    test_data = {
        "name": "Debug User",
        "email": "debug@example.com",
        "password": "password123"
    }
    
    print("🔍 Testing registration with detailed error logging...")
    print(f"📤 Data: {json.dumps(test_data, indent=2)}")
    
    try:
        # Test registration
        response = requests.post(
            'http://localhost:5000/auth/register',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"📥 Response: {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            print(f"📥 Raw response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return True
        elif response.status_code == 409:
            print("⚠️ User already exists")
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_server_health():
    """Test if server is responding"""
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        print(f"📥 Health check: {response.status_code} - {response.text}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Exact Error Debug")
    print("=" * 30)
    
    if test_server_health():
        if test_with_detailed_error():
            print("\n✅ Test completed")
        else:
            print("\n❌ Registration test failed")
            print("\n💡 The server is running but returning 500 errors.")
            print("💡 Check the server console for detailed error messages.")
    else:
        print("\n❌ Server not responding") 