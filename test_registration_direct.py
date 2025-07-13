#!/usr/bin/env python3
"""
Test registration logic directly to find the exact error
"""

import os
import sys

# Set environment variables
current_dir = os.getcwd()
db_path = os.path.join(current_dir, 'instance', 'app.db')
db_uri = f'sqlite:///{db_path}'

os.environ['SQLALCHEMY_DATABASE_URI'] = db_uri
os.environ['SECRET_KEY'] = 'supersecretkey'
os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'

def test_registration_step_by_step():
    """Test registration logic step by step"""
    print("🔍 Testing registration step by step...")
    print(f"📁 Database URI: {db_uri}")
    
    try:
        # Step 1: Import modules
        print("\n1️⃣ Importing modules...")
        from main_app.app import create_app
        from main_app.models import db
        from main_app.models.user import User
        from main_app.routes.auth_service import AuthService
        print("✅ All modules imported successfully")
        
        # Step 2: Create app
        print("\n2️⃣ Creating Flask app...")
        app = create_app()
        print("✅ Flask app created")
        
        # Step 3: Test database connection
        print("\n3️⃣ Testing database connection...")
        with app.app_context():
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1')).fetchone()
            print("✅ Database connection successful")
            
            # Step 4: Test user creation
            print("\n4️⃣ Testing user creation...")
            test_data = {
                "name": "Direct Test User",
                "email": "directtest@example.com",
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
            
            print("✅ User object created")
            
            # Add to database
            db.session.add(new_user)
            db.session.commit()
            
            print(f"✅ User saved to database with ID: {new_user.id}")
            print("✅ Registration logic works perfectly!")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_auth_routes():
    """Test auth routes import"""
    print("\n🔍 Testing auth routes...")
    
    try:
        from main_app.routes.auth_routes import auth_bp
        print("✅ Auth blueprint imported successfully")
        
        # Test the register function directly
        from main_app.routes.auth_routes import register
        print("✅ Register function imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Auth routes error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Direct Registration Test")
    print("=" * 40)
    
    if test_auth_routes():
        if test_registration_step_by_step():
            print("\n🎉 Registration logic works!")
            print("💡 The issue might be in the Flask route handling or request processing")
        else:
            print("\n❌ Registration logic failed")
    else:
        print("\n❌ Auth routes failed") 