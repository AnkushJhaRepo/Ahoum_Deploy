#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5000"

def debug_facilitator_auth():
    """Debug the facilitator authentication flow"""
    print("=== Facilitator Authentication Debug ===\n")
    
    # Step 1: Login as facilitator
    print("1. Logging in as facilitator...")
    login_data = {
        "email": "facilitator_gvt2zb@test.com",
        "password": "v0oz2nqGvJ"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"   Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user = data.get('user')
            
            print(f"   ✅ Login successful")
            print(f"   Token: {token[:20]}..." if token else "   ❌ No token")
            print(f"   User: {user.get('name') if user else 'None'}")
            print(f"   Role: {user.get('role') if user else 'None'}")
            
            if not token:
                print("   ❌ No token received - cannot proceed")
                return
            
            # Step 2: Test the dashboard endpoint
            print("\n2. Testing facilitator dashboard endpoint...")
            headers = {'Authorization': f'Bearer {token}'}
            
            dashboard_response = requests.get(f"{BASE_URL}/api/facilitator/dashboard", headers=headers)
            print(f"   Dashboard Status: {dashboard_response.status_code}")
            
            if dashboard_response.status_code == 200:
                dashboard_data = dashboard_response.json()
                print(f"   ✅ Dashboard access successful")
                print(f"   Total Users: {dashboard_data.get('total_users')}")
                print(f"   Total Sessions: {dashboard_data.get('total_sessions')}")
                print(f"   Upcoming Sessions: {dashboard_data.get('upcoming_sessions')}")
                print(f"   Total Bookings: {dashboard_data.get('total_bookings')}")
            elif dashboard_response.status_code == 403:
                print("   ❌ Access denied - 403 Forbidden")
                print(f"   Response: {dashboard_response.text}")
            else:
                print(f"   ❌ Unexpected status: {dashboard_response.status_code}")
                print(f"   Response: {dashboard_response.text}")
            
            # Step 3: Test the dashboard page route
            print("\n3. Testing dashboard page route...")
            page_response = requests.get(f"{BASE_URL}/api/facilitator/dashboard-page")
            print(f"   Page Status: {page_response.status_code}")
            
            if page_response.status_code == 200:
                print(f"   ✅ Dashboard page served successfully")
                print(f"   Content length: {len(page_response.text)} characters")
                if "Facilitator Dashboard" in page_response.text:
                    print("   ✅ HTML contains 'Facilitator Dashboard'")
                else:
                    print("   ❌ HTML does not contain expected content")
            else:
                print(f"   ❌ Page not served: {page_response.status_code}")
            
            # Step 4: Test user profile endpoint
            print("\n4. Testing user profile endpoint...")
            profile_response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
            print(f"   Profile Status: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                print(f"   ✅ Profile access successful")
                print(f"   User ID: {profile_data.get('id')}")
                print(f"   Name: {profile_data.get('name')}")
                print(f"   Email: {profile_data.get('email')}")
                print(f"   Role: {profile_data.get('role')}")
            else:
                print(f"   ❌ Profile access failed: {profile_response.status_code}")
                print(f"   Response: {profile_response.text}")
                
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error during login: {str(e)}")

if __name__ == "__main__":
    debug_facilitator_auth() 