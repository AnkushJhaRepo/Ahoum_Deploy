#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5000"

def test_facilitator_auth_flow():
    """Test the complete facilitator authentication flow"""
    print("Testing facilitator authentication flow...")
    
    # Step 1: Login as a facilitator
    print("\n1. Logging in as facilitator...")
    login_data = {
        "email": "facilitator@test.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user = data.get('user')
            
            if token and user:
                print("   ✅ Login successful")
                print(f"   User role: {user.get('role')}")
                print(f"   Token length: {len(token)}")
                
                # Step 2: Test dashboard API with token
                print("\n2. Testing dashboard API with token...")
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(f"{BASE_URL}/api/facilitator/dashboard", headers=headers)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    dashboard_data = response.json()
                    print("   ✅ Dashboard API access successful")
                    print(f"   Total users: {dashboard_data.get('total_users')}")
                    print(f"   Total sessions: {dashboard_data.get('total_sessions')}")
                else:
                    print("   ❌ Dashboard API access failed")
                    print(f"   Response: {response.text}")
                
                # Step 3: Test dashboard page with token
                print("\n3. Testing dashboard page access...")
                response = requests.get(f"{BASE_URL}/api/facilitator/dashboard-page", headers=headers)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("   ✅ Dashboard page access successful")
                    if "Facilitator Dashboard" in response.text:
                        print("   ✅ HTML content is correct")
                    else:
                        print("   ❌ HTML content is incorrect")
                else:
                    print("   ❌ Dashboard page access failed")
                    print(f"   Response: {response.text}")
                
            else:
                print("   ❌ Login response missing token or user data")
        else:
            print("   ❌ Login failed")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error during login: {e}")

if __name__ == "__main__":
    test_facilitator_auth_flow() 