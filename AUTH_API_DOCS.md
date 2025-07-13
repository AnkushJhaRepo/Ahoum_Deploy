# Authentication API Documentation

This document describes the authentication endpoints available in the Flask application.

## Base URL
All authentication endpoints are prefixed with `/auth`

## Endpoints

### 1. Register User
**POST** `/auth/register`

Register a new user with email and password.

#### Request Body
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

#### Response (201 Created)
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "created_at": "2024-01-01T12:00:00"
    }
}
```

#### Error Responses
- **400 Bad Request**: Missing required fields, invalid email format, or weak password
- **409 Conflict**: User with email already exists
- **500 Internal Server Error**: Server error

### 2. Login User
**POST** `/auth/login`

Authenticate user and return JWT token.

#### Request Body
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```

#### Response (200 OK)
```json
{
    "message": "Login successful",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    }
}
```

#### Error Responses
- **400 Bad Request**: Missing required fields
- **401 Unauthorized**: Invalid email or password
- **500 Internal Server Error**: Server error

### 3. Get User Profile
**GET** `/auth/profile`

Get current user's profile information (requires authentication).

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response (200 OK)
```json
{
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "created_at": "2024-01-01T12:00:00"
    }
}
```

#### Error Responses
- **401 Unauthorized**: Missing or invalid JWT token
- **404 Not Found**: User not found
- **500 Internal Server Error**: Server error

## Validation Rules

### Email Validation
- Must be a valid email format
- Example: `user@example.com`

### Password Validation
- Minimum 8 characters long
- Should be secure (consider adding more validation rules as needed)

## Security Features

1. **Password Hashing**: All passwords are hashed using SHA-256 before storage
2. **JWT Tokens**: Secure token-based authentication
3. **Token Expiration**: JWT tokens expire after 24 hours
4. **Input Validation**: Comprehensive validation for all inputs
5. **Error Handling**: Proper error responses without exposing sensitive information

## Usage Examples

### Using curl

#### Register a user:
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

#### Login:
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

#### Get profile (with token):
```bash
curl -X GET http://localhost:5000/auth/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Using Python requests

```python
import requests

# Register
response = requests.post('http://localhost:5000/auth/register', json={
    'name': 'John Doe',
    'email': 'john@example.com',
    'password': 'securepassword123'
})

# Login
response = requests.post('http://localhost:5000/auth/login', json={
    'email': 'john@example.com',
    'password': 'securepassword123'
})
token = response.json()['access_token']

# Get profile
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5000/auth/profile', headers=headers)
```

## Environment Variables

Make sure to set the following environment variables:

```bash
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
SQLALCHEMY_DATABASE_URI=your_database_uri_here
```

## Testing

Run the test script to verify the endpoints:

```bash
python test_auth.py
```

This will test registration, login, and profile retrieval functionality. 