#!/usr/bin/env python3
"""
Test script for CRM App endpoints
"""

import requests
import json
from datetime import datetime

# Base URL for the CRM service
BASE_URL = "http://localhost:5001"

# Test Bearer token (should match the one configured in the app)
TEST_BEARER_TOKEN = "your-static-bearer-token-here"

def test_health_check():
    """Test health check endpoint"""
    print("Testing GET /health...")
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Service: {data.get('service')}")
        print(f"Status: {data.get('status')}")
        print("✅ Health check successful")
    else:
        print(f"❌ Health check failed: {response.text}")
    
    print("-" * 50)

def test_notify_valid_payload():
    """Test notify endpoint with valid payload"""
    print("Testing POST /notify with valid payload...")
    
    headers = {
        "Authorization": f"Bearer {TEST_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "booking_id": 123,
        "user": {
            "id": 456,
            "name": "John Doe",
            "email": "john@example.com"
        },
        "event": {
            "id": 789,
            "title": "Tech Conference 2024",
            "start_date": "2024-01-15T09:00:00"
        },
        "facilitator_id": 101
    }
    
    response = requests.post(f"{BASE_URL}/notify", json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Message: {data.get('message')}")
        print(f"Booking ID: {data.get('booking_id')}")
        print("✅ Notify with valid payload successful")
    else:
        print(f"❌ Notify failed: {response.text}")
    
    print("-" * 50)

def test_notify_invalid_token():
    """Test notify endpoint with invalid token"""
    print("Testing POST /notify with invalid token...")
    
    headers = {
        "Authorization": "Bearer invalid-token",
        "Content-Type": "application/json"
    }
    
    payload = {
        "booking_id": 123,
        "user": {
            "id": 456,
            "name": "John Doe",
            "email": "john@example.com"
        },
        "event": {
            "id": 789,
            "title": "Tech Conference 2024",
            "start_date": "2024-01-15T09:00:00"
        },
        "facilitator_id": 101
    }
    
    response = requests.post(f"{BASE_URL}/notify", json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ Invalid token correctly rejected")
    else:
        print(f"❌ Expected 401, got {response.status_code}")
    
    print("-" * 50)

def test_notify_missing_token():
    """Test notify endpoint without token"""
    print("Testing POST /notify without token...")
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "booking_id": 123,
        "user": {
            "id": 456,
            "name": "John Doe",
            "email": "john@example.com"
        },
        "event": {
            "id": 789,
            "title": "Tech Conference 2024",
            "start_date": "2024-01-15T09:00:00"
        },
        "facilitator_id": 101
    }
    
    response = requests.post(f"{BASE_URL}/notify", json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ Missing token correctly rejected")
    else:
        print(f"❌ Expected 401, got {response.status_code}")
    
    print("-" * 50)

def test_notify_invalid_payload():
    """Test notify endpoint with invalid payload"""
    print("Testing POST /notify with invalid payload...")
    
    headers = {
        "Authorization": f"Bearer {TEST_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Test missing required field
    payload_missing_field = {
        "booking_id": 123,
        "user": {
            "id": 456,
            "name": "John Doe",
            "email": "john@example.com"
        },
        "event": {
            "id": 789,
            "title": "Tech Conference 2024",
            "start_date": "2024-01-15T09:00:00"
        }
        # Missing facilitator_id
    }
    
    response = requests.post(f"{BASE_URL}/notify", json=payload_missing_field, headers=headers)
    print(f"Missing field - Status Code: {response.status_code}")
    
    if response.status_code == 400:
        data = response.json()
        print(f"Error: {data.get('error')}")
        print("✅ Missing field correctly rejected")
    else:
        print(f"❌ Expected 400, got {response.status_code}")
    
    # Test invalid field type
    payload_invalid_type = {
        "booking_id": "invalid",  # Should be integer
        "user": {
            "id": 456,
            "name": "John Doe",
            "email": "john@example.com"
        },
        "event": {
            "id": 789,
            "title": "Tech Conference 2024",
            "start_date": "2024-01-15T09:00:00"
        },
        "facilitator_id": 101
    }
    
    response = requests.post(f"{BASE_URL}/notify", json=payload_invalid_type, headers=headers)
    print(f"Invalid type - Status Code: {response.status_code}")
    
    if response.status_code == 400:
        data = response.json()
        print(f"Error: {data.get('error')}")
        print("✅ Invalid type correctly rejected")
    else:
        print(f"❌ Expected 400, got {response.status_code}")
    
    print("-" * 50)

def test_notify_non_json():
    """Test notify endpoint with non-JSON payload"""
    print("Testing POST /notify with non-JSON payload...")
    
    headers = {
        "Authorization": f"Bearer {TEST_BEARER_TOKEN}",
        "Content-Type": "text/plain"
    }
    
    response = requests.post(f"{BASE_URL}/notify", data="not json", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 400:
        data = response.json()
        print(f"Error: {data.get('error')}")
        print("✅ Non-JSON payload correctly rejected")
    else:
        print(f"❌ Expected 400, got {response.status_code}")
    
    print("-" * 50)

def test_get_notifications():
    """Test get notifications endpoint"""
    print("Testing GET /notifications...")
    
    response = requests.get(f"{BASE_URL}/notifications")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Notifications count: {data.get('count', 0)}")
        print("✅ Get notifications successful")
    else:
        print(f"❌ Get notifications failed: {response.text}")
    
    print("-" * 50)

def test_error_handling():
    """Test error handling"""
    print("Testing error handling...")
    
    # Test 404
    response = requests.get(f"{BASE_URL}/nonexistent")
    print(f"404 endpoint - Status Code: {response.status_code}")
    
    # Test 405 (wrong method)
    response = requests.get(f"{BASE_URL}/notify")
    print(f"405 method - Status Code: {response.status_code}")
    
    print("✅ Error handling tests completed")
    print("-" * 50)

if __name__ == "__main__":
    print("Testing CRM App Endpoints")
    print("=" * 50)
    
    try:
        # Test all endpoints
        test_health_check()
        test_notify_valid_payload()
        test_notify_invalid_token()
        test_notify_missing_token()
        test_notify_invalid_payload()
        test_notify_non_json()
        test_get_notifications()
        test_error_handling()
        
        print("🎉 All CRM app tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the CRM app is running on http://localhost:5001")
        print("Start the CRM app with: python crm_microservice/crm_app.py")
    except Exception as e:
        print(f"❌ Test failed: {e}") 