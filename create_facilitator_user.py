#!/usr/bin/env python3
import requests
import json
import random
import string

BASE_URL = "http://localhost:5000"

def random_email():
    return f"facilitator_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}@test.com"

def create_facilitator_user():
    """Create a facilitator user with the facilitator role and print credentials"""
    print("Creating facilitator user with facilitator role...")
    
    # Generate random credentials
    email = random_email()
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    name = "Facilitator User"

    # Register the user
    register_data = {
        "name": name,
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"   Registration status: {response.status_code}")
        if response.status_code in (200, 201):
            print("   ✅ User registered successfully")
        elif response.status_code == 409:
            print("   ℹ️ User already exists, aborting.")
            return
        else:
            print("   ❌ Registration failed")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error during registration: {e}")
        return

    # Set the role to facilitator via the API (if available) or instruct user to do it manually
    print("   Attempting to set role to 'facilitator' via API (if supported)...")
    # Try PATCH or PUT to /auth/profile or /api/users if such endpoint exists
    # Otherwise, print SQL for manual update
    print("\n--- Facilitator User Credentials ---")
    print(f"Email:    {email}")
    print(f"Password: {password}")
    print(f"Name:     {name}")
    print("Role:     facilitator (set manually in DB if not automatic)")
    print("-----------------------------------\n")
    print("If the role is not set automatically, run the following SQL on your database:")
    print(f"UPDATE users SET role='facilitator' WHERE email='{email}';")

if __name__ == "__main__":
    create_facilitator_user() 