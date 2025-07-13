#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def create_test_session():
    """Create a test session for the facilitator"""
    print("=== Creating Test Session for Facilitator ===\n")
    
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
            
            if not token:
                print("   ❌ No token received")
                return
            
            print("   ✅ Login successful")
            print(f"   User ID: {user.get('id')}")
            headers = {'Authorization': f'Bearer {token}'}
            
            # Step 2: Check if there are any events
            print("\n2. Checking available events...")
            events_response = requests.get(f"{BASE_URL}/api/events")
            print(f"   Events Status: {events_response.status_code}")
            
            if events_response.status_code == 200:
                events_data = events_response.json()
                events = events_data.get('events', [])
                print(f"   ✅ Found {len(events)} events")
                
                if len(events) == 0:
                    print("   ❌ No events available. Cannot create session without an event.")
                    return
                
                # Use the first event
                event = events[0]
                event_id = event.get('id')
                print(f"   Using event: {event.get('title')} (ID: {event_id})")
                
                # Step 3: Create a test session
                print("\n3. Creating test session...")
                
                # Create a session time in the future (tomorrow)
                tomorrow = datetime.now() + timedelta(days=1)
                session_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0).isoformat()
                
                session_data = {
                    "event_id": event_id,
                    "time": session_time,
                    "location": "Test Room 101",
                    "max_capacity": 20
                }
                
                print(f"   Session data: {session_data}")
                
                # Create session (this would typically be done by an admin, but for testing...)
                # Let me check if there's a session creation endpoint
                session_response = requests.post(f"{BASE_URL}/api/events/{event_id}/sessions", 
                                               json=session_data, headers=headers)
                print(f"   Create Session Status: {session_response.status_code}")
                
                if session_response.status_code == 201:
                    session_info = session_response.json()
                    print(f"   ✅ Session created successfully!")
                    print(f"   Session ID: {session_info.get('session', {}).get('id')}")
                    print(f"   Time: {session_info.get('session', {}).get('time')}")
                    print(f"   Location: {session_info.get('session', {}).get('location')}")
                    
                    # Now test the cancellation
                    session_id = session_info.get('session', {}).get('id')
                    print(f"\n4. Testing session cancellation...")
                    
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
                    print(f"   ❌ Failed to create session")
                    print(f"   Response: {session_response.text}")
                    
            else:
                print(f"   ❌ Failed to get events: {events_response.status_code}")
                print(f"   Response: {events_response.text}")
                
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    create_test_session() 