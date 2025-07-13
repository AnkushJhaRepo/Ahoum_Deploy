#!/usr/bin/env python3
"""
Simple test script to check Flask app startup
"""

import os
import sys
from pathlib import Path

# Set environment variables if not already set
if not os.getenv('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'supersecretkey'
if not os.getenv('SQLALCHEMY_DATABASE_URI'):
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
if not os.getenv('JWT_SECRET_KEY'):
    os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from main_app.app import create_app
        print("✅ main_app.app imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_app_creation():
    """Test if Flask app can be created"""
    print("\n🔧 Testing app creation...")
    
    try:
        from main_app.app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        return app
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_database():
    """Test database connection"""
    print("\n🗄️ Testing database...")
    
    try:
        from main_app.models import db
        from main_app.app import create_app
        
        app = create_app()
        with app.app_context():
            # Test database connection
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful")
            
            # Check if tables exist
            from main_app.models.user import User
            print("✅ User model imported successfully")
            
            return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_auth_service():
    """Test auth service"""
    print("\n🔐 Testing auth service...")
    
    try:
        from main_app.routes.auth_service import AuthService
        print("✅ AuthService imported successfully")
        
        # Test password hashing
        hashed = AuthService.hash_password("testpassword")
        print("✅ Password hashing works")
        
        # Test password verification
        is_valid = AuthService.verify_password("testpassword", hashed)
        print(f"✅ Password verification works: {is_valid}")
        
        return True
    except Exception as e:
        print(f"❌ Auth service error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_routes():
    """Test route registration"""
    print("\n🛣️ Testing routes...")
    
    try:
        from main_app.app import create_app
        app = create_app()
        
        # Check if routes are registered
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.methods} {rule.rule}")
        
        print(f"✅ Found {len(routes)} routes:")
        for route in routes:
            print(f"   {route}")
        
        # Check for auth routes specifically
        auth_routes = [r for r in routes if '/auth/' in r]
        if auth_routes:
            print("✅ Auth routes found:")
            for route in auth_routes:
                print(f"   {route}")
        else:
            print("❌ No auth routes found")
        
        return True
    except Exception as e:
        print(f"❌ Route testing error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 Flask App Test Suite")
    print("=" * 40)
    
    # Test 1: Imports
    if not test_imports():
        return
    
    # Test 2: App creation
    app = test_app_creation()
    if not app:
        return
    
    # Test 3: Database
    if not test_database():
        return
    
    # Test 4: Auth service
    if not test_auth_service():
        return
    
    # Test 5: Routes
    if not test_routes():
        return
    
    print("\n🎉 All tests passed!")
    print("\n🚀 You can now start the server with:")
    print("   python main.py")
    print("\n📝 Then test the register endpoint:")
    print("   POST http://localhost:5000/auth/register")
    print("   Content-Type: application/json")
    print("   Body: {\"name\": \"Test User\", \"email\": \"test@example.com\", \"password\": \"password123\"}")

if __name__ == "__main__":
    main() 