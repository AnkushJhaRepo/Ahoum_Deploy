#!/usr/bin/env python3
"""
Test script for CRM booking notifications
This script tests the integration between the main app and CRM microservice
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
MAIN_APP_URL = "http://localhost:5000"
CRM_URL = "http://localhost:5001"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword123"

def test_crm_connection():
    """Test if CRM service is running"""
    print("🔍 Testing CRM service connection...")
    try:
        response = requests.get(f"{CRM_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ CRM service is running")
            return True
        else:
            print(f"❌ CRM service returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to CRM service: {e}")
        return False

def test_user_login():
    """Test user login to get JWT token"""
    print("\n🔐 Testing user login...")
    
    # First, try to register the user
    register_data = {
        "name": "Test User",
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    try:
        response = requests.post(f"{MAIN_APP_URL}/auth/register", json=register_data)
        if response.status_code in [201, 409]:  # Created or already exists
            print("✅ User registration successful or user already exists")
        else:
            print(f"⚠️ Registration returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️ Registration failed: {e}")
    
    # Now try to login
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    try:
        response = requests.post(f"{MAIN_APP_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            if token:
                print("✅ Login successful, got JWT token")
                return token
            else:
                print("❌ No access token in response")
                return None
        else:
            print(f"❌ Login failed with status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login request failed: {e}")
        return None

def test_booking_with_notification(token):
    """Test booking a session and verify CRM notification"""
    print("\n📅 Testing session booking with CRM notification...")
    
    # Get available events
    try:
        response = requests.get(f"{MAIN_APP_URL}/events")
        if response.status_code != 200:
            print(f"❌ Failed to get events: {response.status_code}")
            return False
        
        events = response.json()
        if not events:
            print("❌ No events available for booking")
            return False
        
        # Get the first event with sessions
        event = None
        for e in events:
            if e.get('sessions') and len(e['sessions']) > 0:
                event = e
                break
        
        if not event:
            print("❌ No events with sessions available")
            return False
        
        session = event['sessions'][0]
        print(f"✅ Found session: {session.get('facilitator_name', 'Unknown')} at {session.get('location', 'Unknown location')}")
        
        # Book the session
        headers = {"Authorization": f"Bearer {token}"}
        booking_data = {"session_id": session['id']}
        
        response = requests.post(f"{MAIN_APP_URL}/bookings/book", json=booking_data, headers=headers)
        
        if response.status_code in [201, 200]:  # Created or reactivated
            booking_result = response.json()
            print(f"✅ Session booked successfully: {booking_result.get('message')}")
            
            # Wait a moment for the notification to be processed
            time.sleep(2)
            
            # Check CRM notifications
            return check_crm_notifications(booking_result.get('booking', {}).get('id'))
        else:
            print(f"❌ Booking failed with status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Booking test failed: {e}")
        return False

def check_crm_notifications(booking_id):
    """Check if the booking notification was received by CRM"""
    print(f"\n📋 Checking CRM notifications for booking {booking_id}...")
    
    try:
        response = requests.get(f"{CRM_URL}/notifications")
        if response.status_code == 200:
            data = response.json()
            notifications = data.get('notifications', [])
            
            # Look for our booking notification
            for notification in notifications:
                notification_data = notification.get('data', {})
                if notification_data.get('booking_id') == booking_id:
                    print("✅ CRM notification found!")
                    print(f"   User: {notification_data.get('user', {}).get('name')}")
                    print(f"   Event: {notification_data.get('event', {}).get('title')}")
                    print(f"   Facilitator ID: {notification_data.get('facilitator_id')}")
                    print(f"   Timestamp: {notification.get('timestamp')}")
                    return True
            
            print("❌ CRM notification not found")
            print(f"   Total notifications: {len(notifications)}")
            if notifications:
                print("   Recent notifications:")
                for i, notif in enumerate(notifications[-3:], 1):
                    print(f"   {i}. Booking {notif.get('data', {}).get('booking_id')} at {notif.get('timestamp')}")
            return False
        else:
            print(f"❌ Failed to get CRM notifications: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking CRM notifications: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting CRM Booking Notification Test")
    print("=" * 50)
    
    # Test 1: Check CRM service
    if not test_crm_connection():
        print("\n❌ CRM service is not available. Please start the CRM microservice first:")
        print("   cd crm_microservice")
        print("   python crm_app.py")
        return False
    
    # Test 2: User authentication
    token = test_user_login()
    if not token:
        print("\n❌ User authentication failed. Please check if the main app is running.")
        return False
    
    # Test 3: Booking with notification
    if test_booking_with_notification(token):
        print("\n🎉 All tests passed! CRM notifications are working correctly.")
        return True
    else:
        print("\n❌ Booking notification test failed.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 