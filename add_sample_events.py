#!/usr/bin/env python3
"""
Script to add sample events to the database
"""

import sys
import os
from datetime import datetime, timedelta

# Add the main_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main_app'))

def add_sample_events():
    """Add sample events to the database"""
    
    try:
        # Import necessary modules
        from main_app.app import create_app
        from main_app.models import db
        from main_app.models.event import Event
        
        # Create Flask app context
        app = create_app()
        
        with app.app_context():
            print("Adding sample events to the database...")
            print("=" * 50)
            
            # Sample events data
            sample_events = [
                {
                    'title': 'Yoga Wellness Retreat',
                    'description': 'Join us for a rejuvenating yoga retreat focused on mindfulness, flexibility, and inner peace. Perfect for beginners and experienced practitioners alike. Includes morning and evening sessions, meditation practices, and healthy meals.',
                    'start_date': datetime.utcnow() + timedelta(days=15),
                    'end_date': datetime.utcnow() + timedelta(days=17)
                },
                {
                    'title': 'Mindfulness Meditation Workshop',
                    'description': 'Learn the art of mindfulness meditation in this comprehensive workshop. Discover techniques for stress reduction, improved focus, and emotional well-being. Suitable for all experience levels.',
                    'start_date': datetime.utcnow() + timedelta(days=8),
                    'end_date': datetime.utcnow() + timedelta(days=8)
                },
                {
                    'title': 'Nature Conservation Awareness Event',
                    'description': 'Explore the importance of nature conservation and sustainable living. Learn about environmental challenges, solutions, and how you can make a difference. Includes expert speakers, interactive sessions, and practical workshops.',
                    'start_date': datetime.utcnow() + timedelta(days=25),
                    'end_date': datetime.utcnow() + timedelta(days=26)
                },
                {
                    'title': 'Digital Wellness & Tech Balance Seminar',
                    'description': 'In our digital age, maintaining a healthy relationship with technology is crucial. This seminar covers digital detox strategies, mindful technology use, and creating healthy boundaries with devices.',
                    'start_date': datetime.utcnow() + timedelta(days=12),
                    'end_date': datetime.utcnow() + timedelta(days=12)
                },
                {
                    'title': 'Creative Arts & Self-Expression Festival',
                    'description': 'Celebrate creativity and self-expression through various art forms including painting, music, dance, and writing. A three-day festival featuring workshops, performances, and collaborative art projects.',
                    'start_date': datetime.utcnow() + timedelta(days=35),
                    'end_date': datetime.utcnow() + timedelta(days=37)
                }
            ]
            
            # Add events to database
            for i, event_data in enumerate(sample_events, 1):
                event = Event()
                event.title = event_data['title']
                event.description = event_data['description']
                event.start_date = event_data['start_date']
                event.end_date = event_data['end_date']
                
                db.session.add(event)
                db.session.commit()
                
                print(f"{i}. ✅ Added: {event.title}")
                print(f"   Start: {event.start_date.strftime('%Y-%m-%d %H:%M')}")
                print(f"   End: {event.end_date.strftime('%Y-%m-%d %H:%M')}")
                print(f"   Status: {'Upcoming' if event.is_upcoming else 'Active' if event.is_active else 'Past'}")
                print()
            
            # Verify events were added
            total_events = Event.query.count()
            print(f"🎉 Successfully added {len(sample_events)} sample events!")
            print(f"📊 Total events in database: {total_events}")
            
            # Show upcoming events
            upcoming_events = Event.query.filter(Event.start_date > datetime.utcnow()).count()
            print(f"📅 Upcoming events: {upcoming_events}")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and the Flask app is properly configured.")
    except Exception as e:
        print(f"❌ Error adding sample events: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_sample_events() 