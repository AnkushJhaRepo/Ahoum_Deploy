#!/usr/bin/env python3
import requests
import json
import time

def test_booking_flow():
    """Test the complete booking flow to identify reload issues"""
    
    print("🔍 Testing Booking Flow to Identify Reload Issues")
    print("=" * 60)
    
    # Test 1: Check both services are running
    print("\n1. Checking service health...")
    try:
        main_health = requests.get('http://localhost:5000/health', timeout=5)
        crm_health = requests.get('http://localhost:5001/health', timeout=5)
        
        if main_health.status_code == 200 and crm_health.status_code == 200:
            print("✅ Both services are running")
        else:
            print("❌ One or both services are not responding")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Login to get a token
    print("\n2. Logging in to get authentication token...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        login_response = requests.post('http://localhost:5000/auth/login', 
                                     json=login_data, timeout=10)
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get('access_token')
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Test 3: Get events to find a session to book
    print("\n3. Getting events to find a session...")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        events_response = requests.get('http://localhost:5000/api/events', 
                                     headers=headers, timeout=10)
        
        if events_response.status_code == 200:
            events_data = events_response.json()
            events = events_data.get('events', [])
            
            if events:
                # Find first event with sessions
                for event in events:
                    sessions_response = requests.get(f'http://localhost:5000/api/events/{event["id"]}/sessions', 
                                                   headers=headers, timeout=10)
                    if sessions_response.status_code == 200:
                        sessions_data = sessions_response.json()
                        sessions = sessions_data.get('sessions', [])
                        if sessions:
                            session_id = sessions[0]['id']
                            print(f"✅ Found session {session_id} in event {event['id']}")
                            break
                else:
                    print("❌ No sessions found in any events")
                    return False
            else:
                print("❌ No events found")
                return False
        else:
            print(f"❌ Failed to get events: {events_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error getting events: {e}")
        return False
    
    # Test 4: Attempt to book the session
    print(f"\n4. Attempting to book session {session_id}...")
    try:
        booking_data = {"session_id": session_id}
        booking_response = requests.post('http://localhost:5000/api/bookings/book', 
                                       json=booking_data, headers=headers, timeout=15)
        
        print(f"Booking response status: {booking_response.status_code}")
        print(f"Booking response: {booking_response.text}")
        
        if booking_response.status_code in [200, 201, 409]:  # Success or already booked
            print("✅ Booking request completed")
        else:
            print(f"❌ Booking failed with status {booking_response.status_code}")
            
    except Exception as e:
        print(f"❌ Booking error: {e}")
        return False
    
    # Test 5: Check if notifications were sent
    print("\n5. Checking CRM notifications...")
    try:
        notifications_response = requests.get('http://localhost:5001/notifications', timeout=5)
        if notifications_response.status_code == 200:
            notifications_data = notifications_response.json()
            notifications = notifications_data.get('notifications', [])
            print(f"✅ Found {len(notifications)} notifications in CRM")
            
            if notifications:
                latest = notifications[-1]
                print(f"Latest notification: {latest.get('data', {}).get('booking_id')}")
        else:
            print(f"❌ Failed to get notifications: {notifications_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking notifications: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Test completed. Check the server logs for any reload issues.")
    return True

if __name__ == "__main__":
    test_booking_flow() 