import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000/auth"

def test_register():
    """Test user registration"""
    print("Testing user registration...")
    
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)
    
    return response.status_code == 201

def test_login():
    """Test user login"""
    print("Testing user login...")
    
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def test_profile(token):
    """Test getting user profile"""
    if not token:
        print("No token available, skipping profile test")
        return
    
    print("Testing user profile...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

if __name__ == "__main__":
    print("Testing Authentication Endpoints")
    print("=" * 50)
    
    # Test registration
    register_success = test_register()
    
    # Test login
    token = test_login()
    
    # Test profile
    test_profile(token)
    
    print("Testing completed!") 