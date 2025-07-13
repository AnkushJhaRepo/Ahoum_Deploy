#!/usr/bin/env python3
"""
Test script for facilitator features
Tests user management, session management, and facilitator dashboard
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000"
FACILITATOR_EMAIL = "john.facilitator@example.com"
FACILITATOR_PASSWORD = "facilitator123"
REGULAR_USER_EMAIL = "test@example.com"
REGULAR_USER_PASSWORD = "testpassword123"

def test_facilitator_login():
    """Test facilitator login"""
    print("Testing facilitator login...")
    
    login_data = {
        "email": FACILITATOR_EMAIL,
        "password": FACILITATOR_PASSWORD
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user = data.get('user')
            
            if user.get('role') == 'facilitator':
                print("✅ Facilitator login successful")
                return token, user
            else:
                print("❌ User is not a facilitator")
                return None, None
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None, None

def test_view_users(token):
    """Test viewing registered users"""
    print("\nTesting view registered users...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/facilitator/users", 
                              headers={'Authorization': f'Bearer {token}'})
        
        if response.status_code == 200:
            data = response.json()
            users = data.get('users', [])
            print(f"✅ Successfully retrieved {len(users)} users")
            
            # Display first few users
            for i, user in enumerate(users[:3]):
                print(f"   {i+1}. {user['name']} ({user['email']}) - {user['role']}")
            
            return True
        else:
            print(f"❌ Failed to get users: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting users: {e}")
        return False

def test_view_my_sessions(token):
    """Test viewing facilitator's sessions"""
    print("\nTesting view my sessions...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/facilitator/my-sessions", 
                              headers={'Authorization': f'Bearer {token}'})
        
        if response.status_code == 200:
            data = response.json()
            sessions = data.get('sessions', [])
            print(f"✅ Successfully retrieved {len(sessions)} sessions")
            
            # Display sessions
            for i, session in enumerate(sessions):
                event_title = session.get('event', {}).get('title', 'Unknown Event')
                print(f"   {i+1}. {event_title} at {session['location']} - {session['booking_count']} bookings")
            
            return sessions
        else:
            print(f"❌ Failed to get sessions: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting sessions: {e}")
        return []

def test_update_session(token, sessions):
    """Test updating a session"""
    if not sessions:
        print("\n⚠️ No sessions to update")
        return False
    
    print("\nTesting update session...")
    session = sessions[0]  # Use first session
    
    # Update time and location
    new_time = (datetime.utcnow() + timedelta(days=7)).isoformat()
    new_location = "Updated Location - " + datetime.now().strftime("%H:%M:%S")
    
    update_data = {
        "time": new_time,
        "location": new_location
    }
    
    try:
        response = requests.put(f"{BASE_URL}/api/facilitator/sessions/{session['id']}", 
                              headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
                              json=update_data)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Session updated successfully")
            print(f"   New time: {new_time}")
            print(f"   New location: {new_location}")
            return True
        else:
            print(f"❌ Failed to update session: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error updating session: {e}")
        return False

def test_view_session_bookings(token, sessions):
    """Test viewing bookings for a session"""
    if not sessions:
        print("\n⚠️ No sessions to view bookings for")
        return False
    
    print("\nTesting view session bookings...")
    session = sessions[0]  # Use first session
    
    try:
        response = requests.get(f"{BASE_URL}/api/facilitator/sessions/{session['id']}/bookings", 
                              headers={'Authorization': f'Bearer {token}'})
        
        if response.status_code == 200:
            data = response.json()
            bookings = data.get('bookings', [])
            print(f"✅ Successfully retrieved {len(bookings)} bookings for session")
            
            # Display bookings
            for i, booking in enumerate(bookings):
                print(f"   {i+1}. {booking['user_name']} ({booking['user_email']}) - {booking['status']}")
            
            return True
        else:
            print(f"❌ Failed to get bookings: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting bookings: {e}")
        return False

def test_facilitator_dashboard(token):
    """Test facilitator dashboard"""
    print("\nTesting facilitator dashboard...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/facilitator/dashboard", 
                              headers={'Authorization': f'Bearer {token}'})
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard data retrieved successfully")
            print(f"   Total users: {data['total_users']}")
            print(f"   Total sessions: {data['total_sessions']}")
            print(f"   Upcoming sessions: {data['upcoming_sessions']}")
            print(f"   Total bookings: {data['total_bookings']}")
            return True
        else:
            print(f"❌ Failed to get dashboard: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting dashboard: {e}")
        return False

def test_regular_user_access():
    """Test that regular users cannot access facilitator features"""
    print("\nTesting regular user access restrictions...")
    
    # Login as regular user
    login_data = {
        "email": REGULAR_USER_EMAIL,
        "password": REGULAR_USER_PASSWORD
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            
            # Try to access facilitator dashboard
            response = requests.get(f"{BASE_URL}/api/facilitator/dashboard", 
                                  headers={'Authorization': f'Bearer {token}'})
            
            if response.status_code == 403:
                print("✅ Regular user correctly denied access to facilitator features")
                return True
            else:
                print(f"❌ Regular user should be denied access, got: {response.status_code}")
                return False
        else:
            print(f"❌ Regular user login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing regular user access: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Facilitator Features")
    print("=" * 50)
    
    # Test 1: Facilitator login
    token, user = test_facilitator_login()
    if not token:
        print("\n❌ Cannot proceed without facilitator login")
        return False
    
    # Test 2: View users
    if not test_view_users(token):
        print("❌ User viewing failed")
        return False
    
    # Test 3: View sessions
    sessions = test_view_my_sessions(token)
    if sessions is None:
        print("❌ Session viewing failed")
        return False
    
    # Test 4: Update session
    if sessions:
        if not test_update_session(token, sessions):
            print("❌ Session update failed")
            return False
    
    # Test 5: View bookings
    if sessions:
        if not test_view_session_bookings(token, sessions):
            print("❌ Booking viewing failed")
            return False
    
    # Test 6: Dashboard
    if not test_facilitator_dashboard(token):
        print("❌ Dashboard failed")
        return False
    
    # Test 7: Regular user access restrictions
    if not test_regular_user_access():
        print("❌ Access control failed")
        return False
    
    print("\n🎉 All facilitator tests passed!")
    print("\n📋 Facilitator Features Summary:")
    print("   ✅ View registered users")
    print("   ✅ View own sessions")
    print("   ✅ Update session details")
    print("   ✅ View session bookings")
    print("   ✅ Access facilitator dashboard")
    print("   ✅ Proper access control")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 