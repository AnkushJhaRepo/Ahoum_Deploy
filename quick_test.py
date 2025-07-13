#!/usr/bin/env python3
"""
Quick test for registration endpoint
"""

import os
import requests
import json

# Set environment variables
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Ahoum_Assignment\\instance\\app.db'
os.environ['SECRET_KEY'] = 'supersecretkey'
os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'

def test_registration():
    """Test registration with correct configuration"""
    
    # Test data
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }
    
    print("🧪 Testing registration endpoint...")
    print(f"📤 Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            'http://localhost:5000/auth/register',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Registration successful!")
            print(f"📋 Response: {json.dumps(result, indent=2)}")
            return True
        elif response.status_code == 409:
            print("⚠️ User already exists (this is expected if you've tested before)")
            return True
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Quick Registration Test")
    print("=" * 30)
    
    if test_registration():
        print("\n🎉 Registration endpoint is working!")
        print("\n💡 You can now test in Postman:")
        print("   POST http://localhost:5000/auth/register")
        print("   Content-Type: application/json")
        print("   Body: {\"name\": \"Ankush Jha\", \"email\": \"ankush@example.com\", \"password\": \"password123\"}")
    else:
        print("\n❌ Registration endpoint is not working")
        print("💡 Try restarting the server with: python start_server_fixed.py") 