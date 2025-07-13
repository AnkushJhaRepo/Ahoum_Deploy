#!/usr/bin/env python3
"""
Debug registration logic directly
"""

import os
import sys

# Set environment variables
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Ahoum_Assignment\\instance\\app.db'
os.environ['SECRET_KEY'] = 'supersecretkey'
os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'

def test_registration_logic():
    """Test registration logic directly"""
    print("🔍 Testing registration logic directly...")
    
    try:
        from main_app.app import create_app
        from main_app.models import db
        from main_app.models.user import User
        from main_app.routes.auth_service import AuthService
        
        app = create_app()
        
        with app.app_context():
            # Test data
            test_data = {
                "name": "Debug User",
                "email": "debug@example.com",
                "password": "password123"
            }
            
            print("✅ App context created")
            
            # Check if user exists
            existing_user = User.query.filter_by(email=test_data['email']).first()
            if existing_user:
                print("⚠️ User exists, deleting for test...")
                db.session.delete(existing_user)
                db.session.commit()
            
            print("✅ User check completed")
            
            # Test password hashing
            hashed_password = AuthService.hash_password(test_data['password'])
            print("✅ Password hashed successfully")
            
            # Create new user
            new_user = User()
            new_user.name = test_data['name']
            new_user.email = test_data['email']
            new_user.password = hashed_password
            
            print("✅ User object created")
            
            # Add to database
            db.session.add(new_user)
            print("✅ User added to session")
            
            # Commit
            db.session.commit()
            print("✅ User committed to database")
            
            print(f"✅ Registration successful! User ID: {new_user.id}")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_auth_routes():
    """Test auth routes import"""
    print("\n🔍 Testing auth routes import...")
    
    try:
        from main_app.routes.auth_routes import auth_bp
        print("✅ Auth blueprint imported successfully")
        
        print("✅ Auth blueprint imported successfully")
        print("✅ Auth routes should be working")
        
        return True
        
    except Exception as e:
        print(f"❌ Auth routes error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("🐛 Registration Debug")
    print("=" * 30)
    
    if test_auth_routes():
        if test_registration_logic():
            print("\n🎉 Registration logic works!")
            print("💡 The issue might be in the Flask route handling")
        else:
            print("\n❌ Registration logic failed")
    else:
        print("\n❌ Auth routes failed")

if __name__ == "__main__":
    main() 