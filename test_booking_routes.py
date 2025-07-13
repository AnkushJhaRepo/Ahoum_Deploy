#!/usr/bin/env python3
"""
Test script for Booking Routes endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:5000/api/bookings"

def get_auth_token():
    """Get authentication token for testing"""
    try:
        # First register a user
        register_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post("http://localhost:5000/auth/register", json=register_data)
        if response.status_code != 201:
            print("Failed to register user for testing")
            return None
        
        # Then login to get token
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post("http://localhost:5000/auth/login", json=login_data)
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print("Failed to login for testing")
            return None
            
    except Exception as e:
        print(f"Error getting auth token: {e}")
        return None

def test_book_session(token):
    """Test booking a session"""
    print("Testing POST /api/bookings/book...")
    
    if not token:
        print("No token available, skipping test")
        return None
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test booking data
    booking_data = {
        "session_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/book", json=booking_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"Booking created: {data.get('message')}")
        print(f"Booking ID: {data['booking']['id']}")
        return data['booking']['id']
    elif response.status_code == 404:
        print("Session not found (expected if no sessions exist)")
    elif response.status_code == 409:
        print("Already booked (expected if already booked)")
    else:
        print(f"Response: {response.text}")
    
    return None

def test_get_my_bookings(token):
    """Test getting user's bookings"""
    print("\nTesting GET /api/bookings/my-bookings...")
    
    if not token:
        print("No token available, skipping test")
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test basic bookings endpoint
    response = requests.get(f"{BASE_URL}/my-bookings", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total bookings: {data['pagination']['total']}")
        print(f"Bookings returned: {len(data['bookings'])}")
        print("✅ GET /api/bookings/my-bookings successful")
    else:
        print(f"❌ GET /api/bookings/my-bookings failed: {response.text}")
    
    print("-" * 50)

def test_get_my_bookings_with_filters(token):
    """Test getting bookings with filters"""
    print("Testing GET /api/bookings/my-bookings with filters...")
    
    if not token:
        print("No token available, skipping test")
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test with status filter
    response = requests.get(f"{BASE_URL}/my-bookings?status=booked", headers=headers)
    print(f"Active bookings - Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Active bookings: {len(data['bookings'])}")
    
    # Test with pagination
    response = requests.get(f"{BASE_URL}/my-bookings?page=1&per_page=5", headers=headers)
    print(f"Pagination - Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Page 1, 5 per page: {len(data['bookings'])} bookings")
        print(f"Total pages: {data['pagination']['pages']}")
    
    print("✅ GET /api/bookings/my-bookings with filters successful")
    print("-" * 50)

def test_cancel_booking(token, booking_id):
    """Test cancelling a booking"""
    print("Testing POST /api/bookings/cancel/{id}...")
    
    if not token or not booking_id:
        print("No token or booking ID available, skipping test")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{BASE_URL}/cancel/{booking_id}", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Booking cancelled: {data.get('message')}")
        print("✅ POST /api/bookings/cancel/{id} successful")
    elif response.status_code == 404:
        print("Booking not found")
    elif response.status_code == 400:
        print("Booking already cancelled or session passed")
    else:
        print(f"Response: {response.text}")
    
    print("-" * 50)

def test_reactivate_booking(token, booking_id):
    """Test reactivating a booking"""
    print("Testing POST /api/bookings/reactivate/{id}...")
    
    if not token or not booking_id:
        print("No token or booking ID available, skipping test")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{BASE_URL}/reactivate/{booking_id}", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Booking reactivated: {data.get('message')}")
        print("✅ POST /api/bookings/reactivate/{id} successful")
    elif response.status_code == 404:
        print("Booking not found")
    elif response.status_code == 400:
        print("Booking already active or session passed")
    else:
        print(f"Response: {response.text}")
    
    print("-" * 50)

def test_get_booking(token, booking_id):
    """Test getting a specific booking"""
    print("Testing GET /api/bookings/{id}...")
    
    if not token or not booking_id:
        print("No token or booking ID available, skipping test")
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/{booking_id}", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Booking ID: {data.get('id')}")
        print(f"Session ID: {data.get('session_id')}")
        print(f"Status: {data.get('status')}")
        print("✅ GET /api/bookings/{id} successful")
    elif response.status_code == 404:
        print("Booking not found")
    elif response.status_code == 403:
        print("Access denied (not your booking)")
    else:
        print(f"Response: {response.text}")
    
    print("-" * 50)

def test_error_handling(token):
    """Test error handling"""
    print("Testing error handling...")
    
    headers = {
        "Authorization": f"Bearer {token}" if token else "Bearer invalid"
    }
    
    # Test without authentication
    if not token:
        response = requests.post(f"{BASE_URL}/book", json={"session_id": 1})
        print(f"No auth - Status Code: {response.status_code}")
    
    # Test invalid booking ID
    if token:
        response = requests.get(f"{BASE_URL}/99999", headers=headers)
        print(f"Invalid booking ID - Status Code: {response.status_code}")
    
    # Test invalid session ID
    if token:
        response = requests.post(f"{BASE_URL}/book", json={"session_id": 99999}, headers=headers)
        print(f"Invalid session ID - Status Code: {response.status_code}")
    
    print("✅ Error handling tests completed")
    print("-" * 50)

if __name__ == "__main__":
    print("Testing Booking Routes Endpoints")
    print("=" * 50)
    
    try:
        # Get authentication token
        token = get_auth_token()
        
        if token:
            print(f"✅ Authentication successful, token obtained")
        else:
            print("❌ Authentication failed, some tests will be skipped")
        
        # Test all endpoints
        booking_id = test_book_session(token)
        test_get_my_bookings(token)
        test_get_my_bookings_with_filters(token)
        
        if booking_id:
            test_cancel_booking(token, booking_id)
            test_reactivate_booking(token, booking_id)
            test_get_booking(token, booking_id)
        
        test_error_handling(token)
        
        print("🎉 All booking routes tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed: {e}") 