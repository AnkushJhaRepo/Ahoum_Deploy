import requests
import json

def test_registration():
    """Test the registration endpoint"""
    url = "http://localhost:5000/auth/register"
    
    # Test data
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("🔍 Testing registration endpoint...")
    print(f"📡 URL: {url}")
    print(f"📦 Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"📋 Response Body: {json.dumps(response_json, indent=2)}")
        except:
            print(f"📄 Response Text: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server might not be running")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_registration() 