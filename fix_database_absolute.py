#!/usr/bin/env python3
"""
Fix database with absolute path
"""

import os
import sys
from pathlib import Path

# Get absolute path to database
current_dir = os.getcwd()
db_path = os.path.join(current_dir, 'instance', 'app.db')
db_uri = f'sqlite:///{db_path}'

print(f"🔧 Using database URI: {db_uri}")

# Set environment variables
os.environ['SQLALCHEMY_DATABASE_URI'] = db_uri
os.environ['SECRET_KEY'] = 'supersecretkey'
os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'

def test_database():
    """Test database connection"""
    print("🧪 Testing database connection...")
    
    try:
        from main_app.app import create_app
        from main_app.models import db
        
        app = create_app()
        
        with app.app_context():
            # Test connection
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1')).fetchone()
            print("✅ Database connection successful")
            
            # Create tables
            db.create_all()
            print("✅ Database tables created")
            
            return True
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_registration():
    """Test registration process"""
    print("\n🧪 Testing registration...")
    
    try:
        from main_app.app import create_app
        from main_app.models import db
        from main_app.models.user import User
        from main_app.routes.auth_service import AuthService
        
        app = create_app()
        
        with app.app_context():
            # Test data
            test_data = {
                "name": "Ankush Jha",
                "email": "ankush@example.com",
                "password": "password123"
            }
            
            # Check if user exists
            existing_user = User.query.filter_by(email=test_data['email']).first()
            if existing_user:
                print("⚠️ User exists, deleting for test...")
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
            
            print("✅ Registration successful!")
            print(f"   User ID: {new_user.id}")
            print(f"   Name: {new_user.name}")
            print(f"   Email: {new_user.email}")
            
            return True
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("🔧 Database Fix with Absolute Path")
    print("=" * 40)
    
    if test_database():
        if test_registration():
            print("\n🎉 Everything works!")
            print("\n🚀 Now restart your server with the correct database URI:")
            print("   Stop current server (Ctrl+C)")
            print("   Set environment variable: SQLALCHEMY_DATABASE_URI=" + db_uri)
            print("   Run: python main.py")
        else:
            print("\n❌ Registration failed")
    else:
        print("\n❌ Database connection failed")

if __name__ == "__main__":
    main() 