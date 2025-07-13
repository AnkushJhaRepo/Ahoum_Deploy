#!/usr/bin/env python3
"""
Fix database path and test registration
"""

import os
import sys
from pathlib import Path

# Set the correct database path
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
os.environ['SECRET_KEY'] = 'supersecretkey'
os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'

def fix_database():
    """Fix database path and create tables"""
    print("🔧 Fixing database configuration...")
    
    try:
        from main_app.app import create_app
        from main_app.models import db
        
        app = create_app()
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Test database connection
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1')).fetchone()
            if result:
                print(f"✅ Database connection test: {result[0]}")
            else:
                print("✅ Database connection test: successful")
            
            return True
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_registration():
    """Test the registration endpoint"""
    print("\n🧪 Testing registration endpoint...")
    
    try:
        from main_app.app import create_app
        from main_app.routes.auth_routes import auth_bp
        from main_app.models import db
        from main_app.models.user import User
        
        app = create_app()
        
        with app.app_context():
            # Test data
            test_data = {
                "name": "Ankush Jha",
                "email": "ankush@example.com",
                "password": "password123"
            }
            
            # Create a test request
            from flask import request
            import json
            
            # Simulate the registration process
            from main_app.routes.auth_service import AuthService
            
            # Check if user exists
            existing_user = User.query.filter_by(email=test_data['email']).first()
            if existing_user:
                print("⚠️ User already exists, deleting for test...")
                db.session.delete(existing_user)
                db.session.commit()
            
            # Create new user
            hashed_password = AuthService.hash_password(test_data['password'])
            new_user = User()
            new_user.name = test_data['name']
            new_user.email = test_data['email']
            new_user.password = hashed_password
            
            db.session.add(new_user)
            db.session.commit()
            
            print("✅ Registration test successful!")
            print(f"   User ID: {new_user.id}")
            print(f"   Name: {new_user.name}")
            print(f"   Email: {new_user.email}")
            
            return True
            
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("🔧 Database and Registration Fix")
    print("=" * 40)
    
    # Fix database
    if not fix_database():
        return
    
    # Test registration
    if not test_registration():
        return
    
    print("\n🎉 Everything is working!")
    print("\n🚀 Now restart your server:")
    print("   1. Stop the current server (Ctrl+C)")
    print("   2. Run: python main.py")
    print("   3. Test in Postman: POST http://localhost:5000/auth/register")

if __name__ == "__main__":
    main() 