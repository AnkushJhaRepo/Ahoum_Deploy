#!/usr/bin/env python3
"""
Test the /auth/profile endpoint to verify it returns the role
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_profile_endpoint():
    """Test the profile endpoint"""
    
    print("Testing /auth/profile endpoint...")
    print("=" * 50)
    
    # First, login to get a token
    login_data = {
        "email": "facilitator@test.com",
        "password": "facilitator123"
    }
    
    try:
        # Login
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result.get('access_token')
            print(f"Got token: {token[:20]}...")
            
            # Test profile endpoint
            headers = {"Authorization": f"Bearer {token}"}
            profile_response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
            
            print(f"Profile status: {profile_response.status_code}")
            print("Profile response:")
            print(json.dumps(profile_response.json(), indent=2))
            
            # Check if role is present
            profile_data = profile_response.json()
            user_data = profile_data.get('user', {})
            role = user_data.get('role')
            
            if role:
                print(f"✅ Role found: {role}")
            else:
                print("❌ Role is missing!")
                
        else:
            print(f"Login failed: {login_response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_profile_endpoint() 