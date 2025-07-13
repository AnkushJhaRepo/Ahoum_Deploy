#!/usr/bin/env python3
"""
Test request parsing in Flask route
"""

import os
import sys
from flask import Flask, request, jsonify

# Set environment variables
current_dir = os.getcwd()
db_path = os.path.join(current_dir, 'instance', 'app.db')
db_uri = f'sqlite:///{db_path}'

os.environ['SQLALCHEMY_DATABASE_URI'] = db_uri
os.environ['SECRET_KEY'] = 'supersecretkey'
os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'

def test_request_parsing():
    """Test request parsing in Flask route"""
    print("🔍 Testing request parsing...")
    
    try:
        from main_app.app import create_app
        from main_app.routes.auth_routes import register
        
        app = create_app()
        
        with app.test_request_context(
            '/auth/register',
            method='POST',
            json={
                "name": "Request Test User",
                "email": "requesttest@example.com",
                "password": "password123"
            },
            headers={'Content-Type': 'application/json'}
        ):
            print("✅ Test request context created")
            
            # Test request.get_json()
            data = request.get_json()
            print(f"✅ Request data: {data}")
            
            # Test the register function directly
            response = register()
            print(f"✅ Register function response: {response}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Request Parsing Test")
    print("=" * 30)
    
    if test_request_parsing():
        print("\n✅ Request parsing works!")
    else:
        print("\n❌ Request parsing failed") 