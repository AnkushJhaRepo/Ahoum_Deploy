#!/usr/bin/env python3
"""
Test with detailed error logging
"""

import os
import requests
import json

# Set environment variables
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Ahoum_Assignment\\instance\\app.db'
os.environ['SECRET_KEY'] = 'supersecretkey'
os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'

def test_with_error_details():
    """Test registration and show detailed error"""
    
    test_data = {
        "name": "Error Test User",
        "email": "errortest@example.com",
        "password": "password123"
    }
    
    print("🧪 Testing registration with error details...")
    print(f"📤 Data: {json.dumps(test_data, indent=2)}")
    
    try:
        # First, let's check if the server is responding
        health_response = requests.get('http://localhost:5000/', timeout=5)
        print(f"📥 Health check status: {health_response.status_code}")
        
        # Now test registration
        response = requests.post(
            'http://localhost:5000/auth/register',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📥 Registration status: {response.status_code}")
        print(f"📥 Response headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"📥 Response body: {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            print(f"📥 Response body (raw): {response.text}")
        
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
        print("💡 Make sure the server is running with: python start_server_fixed.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simple_request():
    """Test a simple request to see if server is working"""
    print("\n🔍 Testing simple request...")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        print(f"📥 Simple request status: {response.status_code}")
        print(f"📥 Response: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Simple request failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Registration Error Debug")
    print("=" * 30)
    
    if test_simple_request():
        if test_with_error_details():
            print("\n✅ Test completed")
        else:
            print("\n❌ Registration test failed")
    else:
        print("\n❌ Server connection failed") 