#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5000"

def test_facilitator_session_cancel():
    """Test facilitator session cancellation functionality"""
    print("=== Testing Facilitator Session Cancellation ===\n")
    
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
            
            if not token:
                print("   ❌ No token received")
                return
            
            print("   ✅ Login successful")
            headers = {'Authorization': f'Bearer {token}'}
            
            # Step 2: Check facilitator's sessions
            print("\n2. Checking facilitator's sessions...")
            sessions_response = requests.get(f"{BASE_URL}/api/facilitator/my-sessions", headers=headers)
            print(f"   Sessions Status: {sessions_response.status_code}")
            
            if sessions_response.status_code == 200:
                sessions_data = sessions_response.json()
                sessions = sessions_data.get('sessions', [])
                print(f"   ✅ Found {len(sessions)} sessions")
                
                if len(sessions) == 0:
                    print("   ℹ️  No sessions found for this facilitator")
                    print("   You need to create sessions first to test cancellation")
                    return
                
                # Display sessions
                for i, session in enumerate(sessions):
                    print(f"   Session {i+1}:")
                    print(f"     ID: {session.get('id')}")
                    print(f"     Event: {session.get('event', {}).get('title', 'Unknown')}")
                    print(f"     Time: {session.get('time')}")
                    print(f"     Location: {session.get('location')}")
                    print(f"     Bookings: {session.get('booking_count')}")
                    print(f"     Status: {'Past' if session.get('is_past') else 'Upcoming'}")
                    print()
                
                # Step 3: Try to cancel the first upcoming session
                upcoming_sessions = [s for s in sessions if not s.get('is_past')]
                
                if upcoming_sessions:
                    session_to_cancel = upcoming_sessions[0]
                    session_id = session_to_cancel.get('id')
                    
                    print(f"3. Testing cancellation of session {session_id}...")
                    
                    # Check bookings first
                    bookings_response = requests.get(f"{BASE_URL}/api/facilitator/sessions/{session_id}/bookings", headers=headers)
                    if bookings_response.status_code == 200:
                        bookings_data = bookings_response.json()
                        bookings = bookings_data.get('bookings', [])
                        print(f"   Session has {len(bookings)} bookings")
                        
                        for booking in bookings:
                            print(f"     - {booking.get('user_name')} ({booking.get('user_email')}) - {booking.get('status')}")
                    
                    # Attempt to cancel the session
                    cancel_response = requests.post(f"{BASE_URL}/api/facilitator/sessions/{session_id}/cancel", headers=headers)
                    print(f"   Cancel Status: {cancel_response.status_code}")
                    
                    if cancel_response.status_code == 200:
                        cancel_data = cancel_response.json()
                        print(f"   ✅ Session cancelled successfully!")
                        print(f"   Message: {cancel_data.get('message')}")
                        print(f"   Cancelled bookings: {cancel_data.get('cancelled_bookings')}")
                    else:
                        print(f"   ❌ Failed to cancel session")
                        print(f"   Response: {cancel_response.text}")
                else:
                    print("   ℹ️  No upcoming sessions to cancel")
                    
            else:
                print(f"   ❌ Failed to get sessions: {sessions_response.status_code}")
                print(f"   Response: {sessions_response.text}")
                
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    test_facilitator_session_cancel() 