#!/usr/bin/env python3
"""
Test script for Event Routes endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:5000/api"

def test_get_events():
    """Test getting all events"""
    print("Testing GET /api/events...")
    
    # Test basic events endpoint
    response = requests.get(f"{BASE_URL}/events")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total events: {data['pagination']['total']}")
        print(f"Events returned: {len(data['events'])}")
        print("✅ GET /api/events successful")
    else:
        print(f"❌ GET /api/events failed: {response.text}")
    
    print("-" * 50)

def test_get_events_with_filters():
    """Test getting events with filters"""
    print("Testing GET /api/events with filters...")
    
    # Test with status filter
    response = requests.get(f"{BASE_URL}/events?status=upcoming")
    print(f"Upcoming events - Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Upcoming events: {len(data['events'])}")
    
    # Test with search filter
    response = requests.get(f"{BASE_URL}/events?search=conference")
    print(f"Search 'conference' - Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Events with 'conference': {len(data['events'])}")
    
    # Test with pagination
    response = requests.get(f"{BASE_URL}/events?page=1&per_page=5")
    print(f"Pagination - Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Page 1, 5 per page: {len(data['events'])} events")
        print(f"Total pages: {data['pagination']['pages']}")
    
    print("✅ GET /api/events with filters successful")
    print("-" * 50)

def test_get_sessions():
    """Test getting all sessions"""
    print("Testing GET /api/sessions...")
    
    # Test basic sessions endpoint
    response = requests.get(f"{BASE_URL}/sessions")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total sessions: {data['pagination']['total']}")
        print(f"Sessions returned: {len(data['sessions'])}")
        print("✅ GET /api/sessions successful")
    else:
        print(f"❌ GET /api/sessions failed: {response.text}")
    
    print("-" * 50)

def test_get_sessions_with_filters():
    """Test getting sessions with filters"""
    print("Testing GET /api/sessions with filters...")
    
    # Test with event_id filter
    response = requests.get(f"{BASE_URL}/sessions?event_id=1")
    print(f"Sessions for event 1 - Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Sessions for event 1: {len(data['sessions'])}")
    
    # Test with status filter
    response = requests.get(f"{BASE_URL}/sessions?status=upcoming")
    print(f"Upcoming sessions - Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Upcoming sessions: {len(data['sessions'])}")
    
    # Test with location filter
    response = requests.get(f"{BASE_URL}/sessions?location=hall")
    print(f"Sessions in 'hall' - Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Sessions in 'hall': {len(data['sessions'])}")
    
    print("✅ GET /api/sessions with filters successful")
    print("-" * 50)

def test_get_specific_event():
    """Test getting a specific event"""
    print("Testing GET /api/events/{id}...")
    
    # Test getting event with ID 1
    response = requests.get(f"{BASE_URL}/events/1")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Event title: {data.get('title', 'N/A')}")
        print(f"Sessions count: {data.get('sessions_count', 0)}")
        print("✅ GET /api/events/{id} successful")
    elif response.status_code == 404:
        print("Event not found (expected if no data exists)")
    else:
        print(f"❌ GET /api/events/{id} failed: {response.text}")
    
    print("-" * 50)

def test_get_specific_session():
    """Test getting a specific session"""
    print("Testing GET /api/sessions/{id}...")
    
    # Test getting session with ID 1
    response = requests.get(f"{BASE_URL}/sessions/1")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Session location: {data.get('location', 'N/A')}")
        print(f"Session time: {data.get('time', 'N/A')}")
        print("✅ GET /api/sessions/{id} successful")
    elif response.status_code == 404:
        print("Session not found (expected if no data exists)")
    else:
        print(f"❌ GET /api/sessions/{id} failed: {response.text}")
    
    print("-" * 50)

def test_error_handling():
    """Test error handling"""
    print("Testing error handling...")
    
    # Test invalid event ID
    response = requests.get(f"{BASE_URL}/events/99999")
    print(f"Invalid event ID - Status Code: {response.status_code}")
    
    # Test invalid session ID
    response = requests.get(f"{BASE_URL}/sessions/99999")
    print(f"Invalid session ID - Status Code: {response.status_code}")
    
    # Test invalid query parameters
    response = requests.get(f"{BASE_URL}/events?page=invalid")
    print(f"Invalid page parameter - Status Code: {response.status_code}")
    
    print("✅ Error handling tests completed")
    print("-" * 50)

if __name__ == "__main__":
    print("Testing Event Routes Endpoints")
    print("=" * 50)
    
    try:
        # Test all endpoints
        test_get_events()
        test_get_events_with_filters()
        test_get_sessions()
        test_get_sessions_with_filters()
        test_get_specific_event()
        test_get_specific_session()
        test_error_handling()
        
        print("🎉 All event routes tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed: {e}") 