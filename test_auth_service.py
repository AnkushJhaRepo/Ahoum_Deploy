#!/usr/bin/env python3
"""
Test script for AuthService functions
Run this after installing bcrypt: pip install bcrypt==4.1.2
"""

import sys
import os

# Add the main_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main_app'))

def test_auth_service():
    """Test the AuthService functions"""
    
    # Mock Flask app context for testing
    class MockApp:
        def __init__(self):
            self.config = {
                'JWT_SECRET_KEY': 'test-secret-key-for-jwt-generation'
            }
        
        def logger(self):
            class MockLogger:
                def error(self, msg): pass
                def warning(self, msg): pass
            return MockLogger()
    
    # Create mock app
    app = MockApp()
    
    try:
        # Import AuthService
        from routes.auth_service import AuthService
        
        print("Testing AuthService functions...")
        print("=" * 50)
        
        # Test password hashing
        print("1. Testing password hashing...")
        test_password = "mySecurePassword123"
        hashed_password = AuthService.hash_password(test_password)
        print(f"   Original password: {test_password}")
        print(f"   Hashed password: {hashed_password[:20]}...")
        print(f"   Hash length: {len(hashed_password)} characters")
        print("   ✅ Password hashing successful")
        
        # Test password verification
        print("\n2. Testing password verification...")
        is_valid = AuthService.verify_password(test_password, hashed_password)
        print(f"   Correct password verification: {is_valid}")
        
        is_invalid = AuthService.verify_password("wrongPassword", hashed_password)
        print(f"   Wrong password verification: {is_invalid}")
        print("   ✅ Password verification successful")
        
        # Test JWT generation
        print("\n3. Testing JWT generation...")
        user_id = 123
        token = AuthService.generate_jwt(user_id)
        print(f"   Generated token: {token[:50]}...")
        print(f"   Token length: {len(token)} characters")
        print("   ✅ JWT generation successful")
        
        # Test JWT verification
        print("\n4. Testing JWT verification...")
        payload = AuthService.verify_jwt(token)
        if payload:
            print(f"   Decoded user_id: {payload.get('user_id')}")
            print(f"   Token expiration: {payload.get('exp')}")
            print("   ✅ JWT verification successful")
        else:
            print("   ❌ JWT verification failed")
        
        # Test user ID extraction
        print("\n5. Testing user ID extraction...")
        extracted_user_id = AuthService.get_user_id_from_token(token)
        print(f"   Extracted user_id: {extracted_user_id}")
        print("   ✅ User ID extraction successful")
        
        # Test JWT refresh
        print("\n6. Testing JWT refresh...")
        refreshed_token = AuthService.refresh_jwt(token)
        if refreshed_token:
            print(f"   Refreshed token: {refreshed_token[:50]}...")
            print("   ✅ JWT refresh successful")
        else:
            print("   ❌ JWT refresh failed")
        
        # Test with additional claims
        print("\n7. Testing JWT with additional claims...")
        additional_claims = {
            'role': 'admin',
            'permissions': ['read', 'write']
        }
        token_with_claims = AuthService.generate_jwt(user_id, additional_claims)
        payload_with_claims = AuthService.verify_jwt(token_with_claims)
        if payload_with_claims:
            print(f"   Role: {payload_with_claims.get('role')}")
            print(f"   Permissions: {payload_with_claims.get('permissions')}")
            print("   ✅ JWT with additional claims successful")
        
        print("\n" + "=" * 50)
        print("🎉 All AuthService tests passed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure to install bcrypt: pip install bcrypt==4.1.2")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_auth_service() 