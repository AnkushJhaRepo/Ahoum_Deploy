# CRM App API Documentation

This document describes the CRM Notification Service API endpoints.

## Overview

The CRM Notification Service is a Flask microservice that handles booking notifications. It validates incoming data, stores notifications, and provides logging capabilities.

## Base URL
The service runs on `http://localhost:5001` by default.

## Authentication
The service uses static Bearer token authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-static-bearer-token>
```

## Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `CRM_BEARER_TOKEN` | Static Bearer token for authentication | `your-static-bearer-token-here` |
| `NOTIFICATION_LOG_FILE` | File to store notifications | `notifications.json` |
| `CRM_PORT` | Port to run the service on | `5001` |
| `CRM_DEBUG` | Enable debug mode | `False` |

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the service is running.

#### Response (200 OK)
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:00:00",
    "service": "crm-notification-service"
}
```

### 2. Send Notification
**POST** `/notify`

Send a booking notification to the CRM service.

#### Headers
```
Authorization: Bearer <your-static-bearer-token>
Content-Type: application/json
```

#### Request Body
```json
{
    "booking_id": 123,
    "user": {
        "id": 456,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "event": {
        "id": 789,
        "title": "Tech Conference 2024",
        "start_date": "2024-01-15T09:00:00"
    },
    "facilitator_id": 101
}
```

#### Field Validation

##### Required Fields
- `booking_id` (integer): Positive integer
- `user` (object): User information
- `event` (object): Event information
- `facilitator_id` (integer): Positive integer

##### User Object Requirements
- `id` (integer): Positive integer
- `name` (string): Non-empty string
- `email` (string): Non-empty string

##### Event Object Requirements
- `id` (integer): Positive integer
- `title` (string): Non-empty string
- `start_date` (string): Non-empty string (ISO format recommended)

#### Response (200 OK)
```json
{
    "message": "Notification processed successfully",
    "booking_id": 123,
    "timestamp": "2024-01-15T10:00:00"
}
```

#### Error Responses
- **400 Bad Request**: Invalid payload, missing fields, wrong data types
- **401 Unauthorized**: Invalid or missing Bearer token
- **500 Internal Server Error**: Server error

### 3. Get Notifications
**GET** `/notifications`

Retrieve all stored notifications (for debugging/monitoring).

#### Response (200 OK)
```json
{
    "notifications": [
        {
            "timestamp": "2024-01-15T10:00:00",
            "data": {
                "booking_id": 123,
                "user": {
                    "id": 456,
                    "name": "John Doe",
                    "email": "john@example.com"
                },
                "event": {
                    "id": 789,
                    "title": "Tech Conference 2024",
                    "start_date": "2024-01-15T09:00:00"
                },
                "facilitator_id": 101
            }
        }
    ],
    "count": 1
}
```

## Validation Rules

### Payload Validation
1. **Required Fields**: All required fields must be present
2. **Data Types**: Fields must have correct data types
3. **Positive Integers**: ID fields must be positive integers
4. **Non-empty Strings**: String fields must not be empty
5. **Object Structure**: Nested objects must have required fields

### Authentication Validation
1. **Bearer Token**: Authorization header must start with "Bearer "
2. **Token Match**: Token must match the configured static token
3. **Header Presence**: Authorization header must be present

## Logging

The service provides comprehensive logging:

### Log Files
- **Application Logs**: `crm_notifications.log`
- **Notification Storage**: `notifications.json` (configurable)

### Log Levels
- **INFO**: Successful operations, startup information
- **WARNING**: Invalid requests, authentication failures
- **ERROR**: Server errors, storage failures

### Log Format
```
2024-01-15 10:00:00,123 - __main__ - INFO - Notification processed successfully for booking_id: 123
```

## Usage Examples

### Using curl

#### Health Check:
```bash
curl -X GET http://localhost:5001/health
```

#### Send Notification:
```bash
curl -X POST http://localhost:5001/notify \
  -H "Authorization: Bearer your-static-bearer-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 123,
    "user": {
        "id": 456,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "event": {
        "id": 789,
        "title": "Tech Conference 2024",
        "start_date": "2024-01-15T09:00:00"
    },
    "facilitator_id": 101
  }'
```

#### Get Notifications:
```bash
curl -X GET http://localhost:5001/notifications
```

### Using Python requests

```python
import requests

# Configuration
BASE_URL = "http://localhost:5001"
BEARER_TOKEN = "your-static-bearer-token-here"

headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}',
    'Content-Type': 'application/json'
}

# Health check
response = requests.get(f"{BASE_URL}/health")
print(f"Health: {response.json()}")

# Send notification
payload = {
    "booking_id": 123,
    "user": {
        "id": 456,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "event": {
        "id": 789,
        "title": "Tech Conference 2024",
        "start_date": "2024-01-15T09:00:00"
    },
    "facilitator_id": 101
}

response = requests.post(f"{BASE_URL}/notify", json=payload, headers=headers)
if response.status_code == 200:
    print("Notification sent successfully")
else:
    print(f"Error: {response.json()}")

# Get notifications
response = requests.get(f"{BASE_URL}/notifications")
notifications = response.json()
print(f"Total notifications: {notifications['count']}")
```

### Using JavaScript fetch

```javascript
const BASE_URL = 'http://localhost:5001';
const BEARER_TOKEN = 'your-static-bearer-token-here';

const headers = {
    'Authorization': `Bearer ${BEARER_TOKEN}`,
    'Content-Type': 'application/json'
};

// Health check
fetch(`${BASE_URL}/health`)
    .then(response => response.json())
    .then(data => console.log('Health:', data));

// Send notification
const payload = {
    booking_id: 123,
    user: {
        id: 456,
        name: "John Doe",
        email: "john@example.com"
    },
    event: {
        id: 789,
        title: "Tech Conference 2024",
        start_date: "2024-01-15T09:00:00"
    },
    facilitator_id: 101
};

fetch(`${BASE_URL}/notify`, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(payload)
})
.then(response => response.json())
.then(data => console.log('Notification result:', data));

// Get notifications
fetch(`${BASE_URL}/notifications`)
    .then(response => response.json())
    .then(data => console.log('Notifications:', data));
```

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
    "error": "Missing required field: booking_id"
}
```

#### 401 Unauthorized
```json
{
    "error": "Unauthorized"
}
```

#### 404 Not Found
```json
{
    "error": "Endpoint not found"
}
```

#### 405 Method Not Allowed
```json
{
    "error": "Method not allowed"
}
```

#### 500 Internal Server Error
```json
{
    "error": "Internal server error"
}
```

## Running the Service

### Development
```bash
cd crm_microservice
python crm_app.py
```

### Production
```bash
# Set environment variables
export CRM_BEARER_TOKEN="your-secure-token-here"
export CRM_PORT=5001
export CRM_DEBUG=false

# Run the service
python crm_app.py
```

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 crm_app:app
```

## Testing

Run the test script to verify the service works correctly:

```bash
python test_crm_app.py
```

This will test all endpoints with various scenarios including:
- Valid notifications
- Invalid authentication
- Invalid payloads
- Error handling

## Security Considerations

1. **Token Security**: Use a strong, unique Bearer token in production
2. **HTTPS**: Use HTTPS in production environments
3. **Rate Limiting**: Consider implementing rate limiting for the `/notify` endpoint
4. **Input Validation**: All inputs are validated to prevent injection attacks
5. **Logging**: Sensitive data is not logged, only metadata

## Monitoring

### Health Checks
- Use `/health` endpoint for load balancer health checks
- Monitor application logs for errors
- Check notification storage file size

### Metrics to Monitor
- Number of notifications processed
- Response times
- Error rates
- Authentication failures

## Integration with Main Application

To integrate with the main booking application, call the CRM service when a booking is created:

```python
# In booking_routes.py after successful booking
import requests

def notify_crm_service(booking, user, session):
    crm_payload = {
        "booking_id": booking.id,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        },
        "event": {
            "id": session.event.id,
            "title": session.event.title,
            "start_date": session.event.start_date.isoformat()
        },
        "facilitator_id": session.facilitator_id
    }
    
    headers = {
        'Authorization': 'Bearer your-crm-token-here',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post('http://localhost:5001/notify', 
                               json=crm_payload, headers=headers)
        if response.status_code == 200:
            print("CRM notification sent successfully")
        else:
            print(f"CRM notification failed: {response.text}")
    except Exception as e:
        print(f"Error sending CRM notification: {e}")
``` 