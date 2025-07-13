#!/usr/bin/env python3
"""
Test script for CRM Notification Service

This script demonstrates how to use the CRMNotificationService to send
notifications to the CRM microservice.

Prerequisites:
1. CRM microservice should be running on http://localhost:5001
2. Main Flask app should be running
3. Required environment variables should be set

Usage:
    python test_notify_crm.py
"""

import sys
import os
import requests
import time

# Add the main_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main_app'))

def test_crm_service_health():
    """Test if the CRM microservice is running"""
    try:
        response = requests.get('http://localhost:5001/health', timeout=5)
        if response.status_code == 200:
            print("✅ CRM microservice is running")
            return True
        else:
            print(f"❌ CRM microservice returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to CRM microservice: {e}")
        return False

def test_notification_service():
    """Test the CRM notification service"""
    try:
        from services.notify_crm import CRMNotificationService
        
        # Initialize the service
        crm_service = CRMNotificationService()
        
        print("\n🔧 Testing CRM Notification Service...")
        
        # Test connection
        if crm_service.test_connection():
            print("✅ Connection test successful")
        else:
            print("❌ Connection test failed")
            return False
        
        # Test 1: Send a general notification
        print("\n📤 Test 1: Sending general notification...")
        try:
            result = crm_service.send_notification(
                notification_type="test_notification",
                user_id=1,
                message="This is a test notification from the main app",
                additional_data={"test_key": "test_value"}
            )
            print(f"✅ General notification sent: {result}")
        except Exception as e:
            print(f"❌ General notification failed: {e}")
            return False
        
        # Test 2: Send a booking notification
        print("\n📤 Test 2: Sending booking notification...")
        try:
            result = crm_service.send_booking_notification(
                booking_id=123,
                user_id=1,
                session_id=456,
                action="created",
                additional_data={"session_name": "Test Session"}
            )
            print(f"✅ Booking notification sent: {result}")
        except Exception as e:
            print(f"❌ Booking notification failed: {e}")
            return False
        
        # Test 3: Send an event notification
        print("\n📤 Test 3: Sending event notification...")
        try:
            result = crm_service.send_event_notification(
                event_id=789,
                user_id=1,
                action="created",
                additional_data={"event_name": "Test Event"}
            )
            print(f"✅ Event notification sent: {result}")
        except Exception as e:
            print(f"❌ Event notification failed: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_crm_notifications_endpoint():
    """Test retrieving stored notifications from CRM service"""
    try:
        print("\n📥 Test 4: Retrieving stored notifications...")
        response = requests.get('http://localhost:5001/notifications', timeout=5)
        
        if response.status_code == 200:
            notifications = response.json()
            print(f"✅ Retrieved {len(notifications)} notifications:")
            for i, notification in enumerate(notifications[-3:], 1):  # Show last 3
                print(f"   {i}. {notification.get('notification_type')} - {notification.get('message')}")
        else:
            print(f"❌ Failed to retrieve notifications: {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error retrieving notifications: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 CRM Notification Service Test")
    print("=" * 50)
    
    # Test 1: Check if CRM service is running
    if not test_crm_service_health():
        print("\n❌ CRM microservice is not available. Please start it first:")
        print("   cd crm_microservice")
        print("   python crm_app.py")
        return
    
    # Test 2: Test notification service
    if not test_notification_service():
        print("\n❌ Notification service tests failed")
        return
    
    # Test 3: Retrieve stored notifications
    if not test_crm_notifications_endpoint():
        print("\n❌ Failed to retrieve notifications")
        return
    
    print("\n🎉 All tests completed successfully!")
    print("\n📋 Summary:")
    print("   - CRM microservice is running")
    print("   - Notification service is working")
    print("   - Notifications are being stored")
    print("   - Service can retrieve stored notifications")

if __name__ == "__main__":
    main() 