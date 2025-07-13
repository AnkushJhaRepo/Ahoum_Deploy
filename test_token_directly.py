#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5000"

def test_token_directly():
    """Test the token directly with the facilitator dashboard"""
    print("=== Testing Token Directly ===\n")
    
    # The token you provided
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNiIsInVzZXJfaWQiOjE2LCJpYXQiOjE3NTI0MzA4MjgsImV4cCI6MTc1MjUxNzIyOH0.gURrwyMlQgqWtjeaDjwoquPWj_MCqpI4UT5t0wLgRNs"
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print(f"Token: {token[:50]}...")
    
    # Test 1: Check if token is valid
    print("\n1. Testing token validity...")
    try:
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        print(f"   Profile Status: {response.status_code}")
        
        if response.status_code == 200:
            profile_data = response.json()
            print(f"   ✅ Token is valid")
            print(f"   User ID: {profile_data.get('id')}")
            print(f"   Name: {profile_data.get('name')}")
            print(f"   Email: {profile_data.get('email')}")
            print(f"   Role: {profile_data.get('role')}")
        else:
            print(f"   ❌ Token is invalid: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return
    
    # Test 2: Test facilitator dashboard endpoint
    print("\n2. Testing facilitator dashboard endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/facilitator/dashboard", headers=headers)
        print(f"   Dashboard Status: {response.status_code}")
        
        if response.status_code == 200:
            dashboard_data = response.json()
            print(f"   ✅ Dashboard access successful")
            print(f"   Total Users: {dashboard_data.get('total_users')}")
            print(f"   Total Sessions: {dashboard_data.get('total_sessions')}")
            print(f"   Upcoming Sessions: {dashboard_data.get('upcoming_sessions')}")
            print(f"   Total Bookings: {dashboard_data.get('total_bookings')}")
        else:
            print(f"   ❌ Dashboard access failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 3: Test facilitator sessions endpoint
    print("\n3. Testing facilitator sessions endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/facilitator/my-sessions", headers=headers)
        print(f"   Sessions Status: {response.status_code}")
        
        if response.status_code == 200:
            sessions_data = response.json()
            sessions = sessions_data.get('sessions', [])
            print(f"   ✅ Sessions access successful")
            print(f"   Found {len(sessions)} sessions")
            
            for session in sessions:
                print(f"     - Session {session.get('id')}: {session.get('event', {}).get('title', 'Unknown')}")
        else:
            print(f"   ❌ Sessions access failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    test_token_directly() 