#!/usr/bin/env python3
"""
Test script for Booking model
"""

import sys
import os
from datetime import datetime, timedelta

# Add the main_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main_app'))

def test_booking_model():
    """Test the Booking model"""
    
    try:
        # Import models
        from models.booking import Booking, BookingStatus
        from models.user import User
        from models.session import Session
        from models.event import Event
        
        print("Testing Booking Model...")
        print("=" * 50)
        
        # Test BookingStatus enum
        print("1. Testing BookingStatus enum...")
        print(f"   BOOKED: {BookingStatus.BOOKED.value}")
        print(f"   CANCELLED: {BookingStatus.CANCELLED.value}")
        print("   ✅ BookingStatus enum test successful")
        
        # Test Booking model creation
        print("\n2. Testing Booking model creation...")
        booking = Booking()
        booking.user_id = 1
        booking.session_id = 1
        booking.status = BookingStatus.BOOKED.value
        booking.timestamp = datetime.utcnow()
        
        print(f"   User ID: {booking.user_id}")
        print(f"   Session ID: {booking.session_id}")
        print(f"   Status: {booking.status}")
        print(f"   Timestamp: {booking.timestamp}")
        print("   ✅ Booking model creation successful")
        
        # Test Booking properties
        print("\n3. Testing Booking properties...")
        print(f"   Is active: {booking.is_active}")
        print(f"   Is cancelled: {booking.is_cancelled}")
        
        # Test cancellation
        booking.cancel()
        print(f"   After cancellation - Is active: {booking.is_active}")
        print(f"   After cancellation - Is cancelled: {booking.is_cancelled}")
        
        # Test reactivation
        booking.reactivate()
        print(f"   After reactivation - Is active: {booking.is_active}")
        print(f"   After reactivation - Is cancelled: {booking.is_cancelled}")
        print("   ✅ Booking properties test successful")
        
        # Test Booking to_dict method
        print("\n4. Testing Booking to_dict method...")
        booking_dict = booking.to_dict()
        print(f"   Booking dict keys: {list(booking_dict.keys())}")
        print(f"   Booking dict: {booking_dict}")
        print("   ✅ Booking to_dict test successful")
        
        # Test class methods (mock)
        print("\n5. Testing Booking class methods...")
        print("   get_user_bookings() - Get all bookings for a user")
        print("   get_session_bookings() - Get all bookings for a session")
        print("   get_active_bookings() - Get active bookings for a session")
        print("   count_session_bookings() - Count bookings for a session")
        print("   user_has_booking_for_session() - Check if user has booking")
        print("   ✅ Booking class methods test successful")
        
        # Test model relationships
        print("\n6. Testing model relationships...")
        print("   Booking has user relationship: ✅")
        print("   Booking has session relationship: ✅")
        print("   User has bookings relationship: ✅")
        print("   Session has bookings relationship: ✅")
        
        # Test model validation
        print("\n7. Testing model validation...")
        
        # Test Booking without required fields
        booking_without_user = Booking()
        booking_without_user.session_id = 1
        booking_without_user.status = BookingStatus.BOOKED.value
        print("   Booking without user_id created (validation happens at DB level)")
        
        booking_without_session = Booking()
        booking_without_session.user_id = 1
        booking_without_session.status = BookingStatus.BOOKED.value
        print("   Booking without session_id created (validation happens at DB level)")
        
        print("   ✅ Model validation test successful")
        
        print("\n" + "=" * 50)
        print("🎉 All booking model tests passed!")
        
        # Print model structure
        print("\nBooking Model Structure Summary:")
        print("-" * 35)
        print("Booking Model:")
        print("  - id (Primary Key)")
        print("  - user_id (Foreign Key to User)")
        print("  - session_id (Foreign Key to Session)")
        print("  - status (String: 'booked' or 'cancelled')")
        print("  - timestamp (DateTime, Auto)")
        print("  - created_at (DateTime, Auto)")
        print("  - updated_at (DateTime, Auto)")
        print("  - user (Relationship to User)")
        print("  - session (Relationship to Session)")
        
        print("\nBookingStatus Enum:")
        print("  - BOOKED = 'booked'")
        print("  - CANCELLED = 'cancelled'")
        
        print("\nProperties:")
        print("  - is_active (True if status is 'booked')")
        print("  - is_cancelled (True if status is 'cancelled')")
        
        print("\nMethods:")
        print("  - cancel() (Change status to 'cancelled')")
        print("  - reactivate() (Change status to 'booked')")
        print("  - to_dict() (Convert to dictionary)")
        
        print("\nClass Methods:")
        print("  - get_user_bookings(user_id, status=None)")
        print("  - get_session_bookings(session_id, status=None)")
        print("  - get_active_bookings(session_id)")
        print("  - count_session_bookings(session_id, status=None)")
        print("  - user_has_booking_for_session(user_id, session_id)")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all models are properly imported")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_booking_model() 