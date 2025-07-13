#!/usr/bin/env python3
"""
Script to add facilitator users to the database
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from main_app.app import create_app
from main_app.models import db
from main_app.models.user import User
import bcrypt

def add_facilitators():
    """Add facilitator users to the database"""
    app = create_app()
    
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
        # Sample facilitator data
        facilitators = [
            {
                'name': 'John Smith',
                'email': 'john.facilitator@example.com',
                'password': 'facilitator123',
                'role': 'facilitator'
            },
            {
                'name': 'Sarah Johnson',
                'email': 'sarah.facilitator@example.com',
                'password': 'facilitator123',
                'role': 'facilitator'
            },
            {
                'name': 'Mike Wilson',
                'email': 'mike.facilitator@example.com',
                'password': 'facilitator123',
                'role': 'facilitator'
            }
        ]
        
        added_count = 0
        
        for facilitator_data in facilitators:
            # Check if user already exists
            existing_user = User.query.filter_by(email=facilitator_data['email']).first()
            if existing_user:
                print(f"Facilitator {facilitator_data['email']} already exists, updating role...")
                existing_user.role = 'facilitator'
                db.session.commit()
                added_count += 1
                continue
            
            # Hash password
            password_hash = bcrypt.hashpw(
                facilitator_data['password'].encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            
            # Create new facilitator user
            new_facilitator = User()
            new_facilitator.name = facilitator_data['name']
            new_facilitator.email = facilitator_data['email']
            new_facilitator.password = password_hash
            new_facilitator.role = facilitator_data['role']
            
            db.session.add(new_facilitator)
            added_count += 1
            print(f"Added facilitator: {facilitator_data['email']}")
        
        db.session.commit()
        print(f"\nSuccessfully added/updated {added_count} facilitators!")
        print("\nFacilitator login credentials:")
        print("Email: john.facilitator@example.com")
        print("Password: facilitator123")
        print("\nEmail: sarah.facilitator@example.com")
        print("Password: facilitator123")
        print("\nEmail: mike.facilitator@example.com")
        print("Password: facilitator123")

if __name__ == "__main__":
    add_facilitators() 