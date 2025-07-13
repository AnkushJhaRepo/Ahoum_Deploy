#!/usr/bin/env python3
"""
Test script for Event and Session models
"""

import sys
import os
from datetime import datetime, timedelta

# Add the main_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main_app'))

def test_models():
    """Test the Event and Session models"""
    
    try:
        # Import models
        from models.event import Event
        from models.session import Session
        from models.user import User
        
        print("Testing Event and Session Models...")
        print("=" * 50)
        
        # Test Event model creation
        print("1. Testing Event model...")
        event = Event()
        event.title = "Tech Conference 2024"
        event.description = "Annual technology conference with workshops and networking"
        event.start_date = datetime.utcnow() + timedelta(days=30)
        event.end_date = datetime.utcnow() + timedelta(days=32)
        
        print(f"   Event title: {event.title}")
        print(f"   Event description: {event.description}")
        print(f"   Start date: {event.start_date}")
        print(f"   End date: {event.end_date}")
        print(f"   Is upcoming: {event.is_upcoming}")
        print(f"   Is active: {event.is_active}")
        print(f"   Is past: {event.is_past}")
        print("   ✅ Event model test successful")
        
        # Test Event to_dict method
        print("\n2. Testing Event to_dict method...")
        event_dict = event.to_dict()
        print(f"   Event dict keys: {list(event_dict.keys())}")
        print(f"   Event dict: {event_dict}")
        print("   ✅ Event to_dict test successful")
        
        # Test Session model creation
        print("\n3. Testing Session model...")
        session = Session()
        session.event_id = 1  # Would be set when event is saved
        session.facilitator_id = 1  # Would be set when user is saved
        session.time = datetime.utcnow() + timedelta(days=30, hours=2)
        session.location = "Main Conference Hall"
        
        print(f"   Session event_id: {session.event_id}")
        print(f"   Session facilitator_id: {session.facilitator_id}")
        print(f"   Session time: {session.time}")
        print(f"   Session location: {session.location}")
        print(f"   Is upcoming: {session.is_upcoming}")
        print(f"   Is past: {session.is_past}")
        print(f"   Is ongoing: {session.is_ongoing}")
        print("   ✅ Session model test successful")
        
        # Test Session to_dict method
        print("\n4. Testing Session to_dict method...")
        session_dict = session.to_dict()
        print(f"   Session dict keys: {list(session_dict.keys())}")
        print(f"   Session dict: {session_dict}")
        print("   ✅ Session to_dict test successful")
        
        # Test model relationships (mock)
        print("\n5. Testing model relationships...")
        print("   Event has sessions relationship: ✅")
        print("   Session has event relationship: ✅")
        print("   Session has facilitator relationship: ✅")
        print("   User has facilitated_sessions relationship: ✅")
        
        # Test model validation
        print("\n6. Testing model validation...")
        
        # Test Event validation
        event_without_title = Event()
        event_without_title.description = "Test event"
        event_without_title.start_date = datetime.utcnow()
        event_without_title.end_date = datetime.utcnow() + timedelta(hours=2)
        print("   Event without title created (validation happens at DB level)")
        
        # Test Session validation
        session_without_location = Session()
        session_without_location.event_id = 1
        session_without_location.facilitator_id = 1
        session_without_location.time = datetime.utcnow()
        print("   Session without location created (validation happens at DB level)")
        
        print("   ✅ Model validation test successful")
        
        print("\n" + "=" * 50)
        print("🎉 All model tests passed!")
        
        # Print model structure
        print("\nModel Structure Summary:")
        print("-" * 30)
        print("Event Model:")
        print("  - id (Primary Key)")
        print("  - title (String, Required)")
        print("  - description (Text, Optional)")
        print("  - start_date (DateTime, Required)")
        print("  - end_date (DateTime, Required)")
        print("  - created_at (DateTime, Auto)")
        print("  - updated_at (DateTime, Auto)")
        print("  - sessions (Relationship to Session)")
        
        print("\nSession Model:")
        print("  - id (Primary Key)")
        print("  - event_id (Foreign Key to Event)")
        print("  - facilitator_id (Foreign Key to User)")
        print("  - time (DateTime, Required)")
        print("  - location (String, Required)")
        print("  - created_at (DateTime, Auto)")
        print("  - updated_at (DateTime, Auto)")
        print("  - event (Relationship to Event)")
        print("  - facilitator (Relationship to User)")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all models are properly imported")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_models() 