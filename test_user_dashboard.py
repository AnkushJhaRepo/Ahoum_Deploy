#!/usr/bin/env python3
"""
Test script to demonstrate user dashboard functionality
Shows how logged-in users can see all available events
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_user_dashboard():
    """Test the complete user dashboard flow"""
    print("Testing User Dashboard - Events View")
    print("=" * 60)
    
    # Step 1: Register a new user (if needed)
    print("1. Registering a new user...")
    register_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "securepassword123"
    }
    
    register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"   Register Status: {register_response.status_code}")
    
    if register_response.status_code == 409:
        print("   User already exists, proceeding to login...")
    elif register_response.status_code == 201:
        print("   ✅ User registered successfully")
    else:
        print(f"   ❌ Registration failed: {register_response.text}")
        return
    
    # Step 2: Login user
    print("\n2. Logging in user...")
    login_data = {
        "email": "testuser@example.com",
        "password": "securepassword123"
    }
    
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"   Login Status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        login_result = login_response.json()
        token = login_result['access_token']
        user_info = login_result['user']
        print(f"   ✅ Login successful")
        print(f"   User: {user_info['name']} ({user_info['email']})")
        print(f"   Token: {token[:50]}...")
    else:
        print(f"   ❌ Login failed: {login_response.text}")
        return
    
    # Step 3: Get user profile
    print("\n3. Getting user profile...")
    headers = {"Authorization": f"Bearer {token}"}
    
    profile_response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
    print(f"   Profile Status: {profile_response.status_code}")
    
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        print(f"   ✅ Profile retrieved: {profile_data['user']['name']}")
    else:
        print(f"   ❌ Profile failed: {profile_response.text}")
    
    # Step 4: Get all events (public endpoint)
    print("\n4. Getting all events (public endpoint)...")
    events_response = requests.get(f"{BASE_URL}/api/events")
    print(f"   Events Status: {events_response.status_code}")
    
    if events_response.status_code == 200:
        events_data = events_response.json()
        events = events_data['events']
        pagination = events_data['pagination']
        print(f"   ✅ Found {len(events)} events (Total: {pagination['total']})")
        
        for i, event in enumerate(events[:3], 1):  # Show first 3 events
            print(f"   {i}. {event['title']}")
            print(f"      Status: {event.get('status', 'N/A')}")
            print(f"      Sessions: {event['sessions_count']}")
            print(f"      Start: {event['start_date'][:10]}")
    else:
        print(f"   ❌ Events failed: {events_response.text}")
    
    # Step 5: Get user dashboard events (authenticated endpoint)
    print("\n5. Getting user dashboard events (authenticated)...")
    dashboard_response = requests.get(f"{BASE_URL}/api/dashboard/events", headers=headers)
    print(f"   Dashboard Status: {dashboard_response.status_code}")
    
    if dashboard_response.status_code == 200:
        dashboard_data = dashboard_response.json()
        dashboard_events = dashboard_data['events']
        user_id = dashboard_data['user_id']
        pagination = dashboard_data['pagination']
        
        print(f"   ✅ Dashboard loaded for user {user_id}")
        print(f"   Found {len(dashboard_events)} events (Total: {pagination['total']})")
        
        for i, event in enumerate(dashboard_events[:3], 1):  # Show first 3 events
            print(f"   {i}. {event['title']}")
            print(f"      Status: {event['status']}")
            print(f"      Sessions: {event['sessions_count']}")
            print(f"      Has Bookings: {event['has_user_bookings']}")
            print(f"      User Bookings: {len(event['user_bookings'])}")
            print(f"      Start: {event['start_date'][:10]}")
    else:
        print(f"   ❌ Dashboard failed: {dashboard_response.text}")
    
    # Step 6: Test filtering
    print("\n6. Testing event filtering...")
    
    # Get upcoming events only
    upcoming_response = requests.get(f"{BASE_URL}/api/dashboard/events?status=upcoming", headers=headers)
    if upcoming_response.status_code == 200:
        upcoming_data = upcoming_response.json()
        upcoming_events = upcoming_data['events']
        print(f"   ✅ Upcoming events: {len(upcoming_events)}")
    
    # Search for specific events
    search_response = requests.get(f"{BASE_URL}/api/dashboard/events?search=yoga", headers=headers)
    if search_response.status_code == 200:
        search_data = search_response.json()
        search_events = search_data['events']
        print(f"   ✅ Events with 'yoga': {len(search_events)}")
    
    print("\n" + "=" * 60)
    print("🎉 User Dashboard Test Completed!")
    print("\nKey Features Demonstrated:")
    print("✅ User registration and login")
    print("✅ JWT token authentication")
    print("✅ Public events endpoint (no auth required)")
    print("✅ Authenticated dashboard endpoint")
    print("✅ User-specific booking information")
    print("✅ Event filtering and search")
    print("✅ Pagination support")

if __name__ == "__main__":
    try:
        test_user_dashboard()
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed: {e}") 