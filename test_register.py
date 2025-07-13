#!/usr/bin/env python3
"""
Test script for the register endpoint
"""

import requests
import json
import time

def test_register():
    """Test the register endpoint"""
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    # Test data
    test_data = {
        "name": "Ankush Jha",
        "email": "ankush@example.com",
        "password": "password123"
    }
    
    print(f"📤 Sending POST request to http://localhost:5000/auth/register")
    print(f"📋 Data: {json.dumps(test_data, indent=2)}")
    
    try:
        # Send POST request
        response = requests.post(
            'http://localhost:5000/auth/register',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"\n📥 Response Status: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"📥 Response Body: {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            print(f"📥 Response Body (raw): {response.text}")
        
        if response.status_code == 201:
            print("\n✅ Registration successful!")
        elif response.status_code == 409:
            print("\n⚠️ User already exists!")
        else:
            print(f"\n❌ Registration failed with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection error - server might not be running")
        print("💡 Make sure to run: python main.py")
    except requests.exceptions.Timeout:
        print("\n❌ Request timeout")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

def test_server_health():
    """Test if server is running"""
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ Server is not running")
        return False

if __name__ == "__main__":
    print("🧪 Testing Register Endpoint")
    print("=" * 40)
    
    # First check if server is running
    if test_server_health():
        test_register()
    else:
        print("\n💡 Start the server first:")
        print("   python main.py") 