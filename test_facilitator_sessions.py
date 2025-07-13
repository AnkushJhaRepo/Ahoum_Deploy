#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5000"

def test_facilitator_sessions():
    """Test facilitator login and session access"""
    
    print("Testing Facilitator Sessions...")
    print("=" * 50)
    
    # Login as facilitator
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
            user_info = login_result.get('user')
            
            print(f"✅ Logged in as: {user_info['name']} (ID: {user_info['id']})")
            print(f"Role: {user_info['role']}")
            
            # Get profile to confirm
            headers = {'Authorization': f'Bearer {token}'}
            profile_response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
            print(f"Profile status: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print(f"Profile confirms: {profile['user']['name']} (ID: {profile['user']['id']})")
                
                # Get facilitator's sessions
                sessions_response = requests.get(f"{BASE_URL}/api/facilitator/my-sessions", headers=headers)
                print(f"Sessions status: {sessions_response.status_code}")
                
                if sessions_response.status_code == 200:
                    sessions_data = sessions_response.json()
                    sessions = sessions_data.get('sessions', [])
                    
                    print(f"\n📋 Found {len(sessions)} sessions for this facilitator:")
                    for session in sessions:
                        print(f"  Session {session['id']}: {session.get('title', 'No title')} (Bookings: {session.get('booking_count', 0)})")
                    
                    if sessions:
                        # Test canceling the first session
                        first_session_id = sessions[0]['id']
                        print(f"\n🧪 Testing cancel for session {first_session_id}...")
                        
                        cancel_response = requests.post(f"{BASE_URL}/api/facilitator/sessions/{first_session_id}/cancel", headers=headers)
                        print(f"Cancel status: {cancel_response.status_code}")
                        
                        if cancel_response.status_code == 200:
                            print("✅ Session cancelled successfully!")
                        else:
                            print(f"❌ Cancel failed: {cancel_response.text}")
                    else:
                        print("No sessions found for this facilitator")
                else:
                    print(f"❌ Failed to get sessions: {sessions_response.text}")
            else:
                print(f"❌ Failed to get profile: {profile_response.text}")
        else:
            print(f"❌ Login failed: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_facilitator_sessions() 