#!/usr/bin/env python3
"""
Script to add sample sessions to existing events
"""

import sys
import os
from datetime import datetime, timedelta

# Add the main_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main_app'))

def add_sample_sessions():
    """Add sample sessions to existing events"""
    
    try:
        # Import necessary modules
        from main_app.app import create_app
        from main_app.models import db
        from main_app.models.event import Event
        from main_app.models.session import Session
        from main_app.models.user import User
        
        # Create Flask app context
        app = create_app()
        
        with app.app_context():
            print("Adding sample sessions to events...")
            print("=" * 50)
            
            # Get existing events
            events = Event.query.all()
            if not events:
                print("❌ No events found. Please run add_sample_events.py first.")
                return
            
            # Get or create a facilitator user
            facilitator = User.query.filter_by(email='facilitator@example.com').first()
            if not facilitator:
                facilitator = User()
                facilitator.name = "Event Facilitator"
                facilitator.email = "facilitator@example.com"
                facilitator.password = "facilitator123"  # In real app, this would be hashed
                db.session.add(facilitator)
                db.session.commit()
                print("✅ Created facilitator user")
            
            # Sample sessions data for each event
            sessions_data = {
                "Yoga Wellness Retreat": [
                    {
                        'time': datetime.utcnow() + timedelta(days=15, hours=9),
                        'location': 'Main Yoga Studio',
                        'description': 'Morning Yoga Session - Beginner friendly'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=15, hours=14),
                        'location': 'Garden Pavilion',
                        'description': 'Afternoon Meditation Workshop'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=16, hours=9),
                        'location': 'Main Yoga Studio',
                        'description': 'Advanced Yoga Session'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=16, hours=16),
                        'location': 'Wellness Center',
                        'description': 'Evening Relaxation Session'
                    }
                ],
                "Mindfulness Meditation Workshop": [
                    {
                        'time': datetime.utcnow() + timedelta(days=8, hours=10),
                        'location': 'Meditation Hall',
                        'description': 'Introduction to Mindfulness'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=8, hours=14),
                        'location': 'Meditation Hall',
                        'description': 'Advanced Meditation Techniques'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=8, hours=16),
                        'location': 'Garden Area',
                        'description': 'Walking Meditation Practice'
                    }
                ],
                "Nature Conservation Awareness Event": [
                    {
                        'time': datetime.utcnow() + timedelta(days=25, hours=10),
                        'location': 'Conference Center',
                        'description': 'Keynote: Environmental Challenges'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=25, hours=14),
                        'location': 'Workshop Room A',
                        'description': 'Sustainable Living Workshop'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=26, hours=9),
                        'location': 'Outdoor Garden',
                        'description': 'Tree Planting Activity'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=26, hours=13),
                        'location': 'Conference Center',
                        'description': 'Panel Discussion: Future of Conservation'
                    }
                ],
                "Digital Wellness & Tech Balance Seminar": [
                    {
                        'time': datetime.utcnow() + timedelta(days=12, hours=10),
                        'location': 'Tech Center',
                        'description': 'Digital Detox Strategies'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=12, hours=13),
                        'location': 'Workshop Room B',
                        'description': 'Mindful Technology Use'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=12, hours=15),
                        'location': 'Tech Center',
                        'description': 'Creating Healthy Digital Boundaries'
                    }
                ],
                "Creative Arts & Self-Expression Festival": [
                    {
                        'time': datetime.utcnow() + timedelta(days=35, hours=10),
                        'location': 'Art Studio 1',
                        'description': 'Painting Workshop'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=35, hours=14),
                        'location': 'Music Room',
                        'description': 'Music & Sound Healing'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=36, hours=11),
                        'location': 'Dance Studio',
                        'description': 'Movement & Dance Workshop'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=36, hours=15),
                        'location': 'Writing Room',
                        'description': 'Creative Writing Session'
                    },
                    {
                        'time': datetime.utcnow() + timedelta(days=37, hours=10),
                        'location': 'Main Hall',
                        'description': 'Collaborative Art Project'
                    }
                ]
            }
            
            total_sessions = 0
            
            # Add sessions for each event
            for event in events:
                if event.title in sessions_data:
                    print(f"\n📅 Adding sessions to: {event.title}")
                    
                    for i, session_info in enumerate(sessions_data[event.title], 1):
                        session = Session()
                        session.event_id = event.id
                        session.facilitator_id = facilitator.id
                        session.time = session_info['time']
                        session.location = session_info['location']
                        
                        db.session.add(session)
                        db.session.commit()
                        
                        print(f"   {i}. ✅ {session_info['description']}")
                        print(f"      📍 {session.location} | 🕐 {session.time.strftime('%Y-%m-%d %H:%M')}")
                        total_sessions += 1
                else:
                    print(f"⚠️  No session data for: {event.title}")
            
            # Verify sessions were added
            all_sessions = Session.query.count()
            print(f"\n🎉 Successfully added {total_sessions} sessions!")
            print(f"📊 Total sessions in database: {all_sessions}")
            
            # Show sessions per event
            print(f"\n📋 Sessions per event:")
            for event in events:
                session_count = Session.query.filter_by(event_id=event.id).count()
                print(f"   • {event.title}: {session_count} sessions")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and the Flask app is properly configured.")
    except Exception as e:
        print(f"❌ Error adding sample sessions: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_sample_sessions() 