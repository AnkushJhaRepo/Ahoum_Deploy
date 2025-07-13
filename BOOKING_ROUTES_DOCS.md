# Booking Routes API Documentation

This document describes the Booking API endpoints available in the Flask application.

## Base URL
All booking endpoints are prefixed with `/api/bookings`

## Authentication
All booking endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### 1. Book a Session
**POST** `/api/bookings/book`

Book a session for the authenticated user.

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body
```json
{
    "session_id": 1
}
```

#### Response (201 Created)
```json
{
    "message": "Session booked successfully",
    "booking": {
        "id": 1,
        "user_id": 2,
        "session_id": 1,
        "status": "booked",
        "timestamp": "2024-01-15T10:00:00",
        "created_at": "2024-01-15T09:30:00",
        "updated_at": "2024-01-15T09:30:00",
        "user_name": "John Doe",
        "user_email": "john@example.com",
        "session_time": "2024-01-15T14:00:00",
        "session_location": "Main Conference Hall",
        "event_title": "Tech Conference 2024"
    }
}
```

#### Response (200 OK) - Reactivated Booking
```json
{
    "message": "Booking reactivated successfully",
    "booking": {
        "id": 1,
        "user_id": 2,
        "session_id": 1,
        "status": "booked",
        "timestamp": "2024-01-15T10:00:00",
        "created_at": "2024-01-15T09:30:00",
        "updated_at": "2024-01-15T10:00:00",
        "user_name": "John Doe",
        "user_email": "john@example.com",
        "session_time": "2024-01-15T14:00:00",
        "session_location": "Main Conference Hall",
        "event_title": "Tech Conference 2024"
    }
}
```

#### Error Responses
- **400 Bad Request**: Missing session_id, session has already passed
- **404 Not Found**: Session not found
- **409 Conflict**: User already has an active booking for this session
- **401 Unauthorized**: Invalid or missing JWT token
- **500 Internal Server Error**: Server error

### 2. Get My Bookings
**GET** `/api/bookings/my-bookings`

Get all bookings for the authenticated user with optional filtering and pagination.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Query Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `page` | integer | Page number for pagination | 1 |
| `per_page` | integer | Number of bookings per page | 10 |
| `status` | string | Filter by status: `booked`, `cancelled`, `all` | all |

#### Response (200 OK)
```json
{
    "bookings": [
        {
            "id": 1,
            "user_id": 2,
            "session_id": 1,
            "status": "booked",
            "timestamp": "2024-01-15T10:00:00",
            "created_at": "2024-01-15T09:30:00",
            "updated_at": "2024-01-15T09:30:00",
            "user_name": "John Doe",
            "user_email": "john@example.com",
            "session_time": "2024-01-15T14:00:00",
            "session_location": "Main Conference Hall",
            "event_title": "Tech Conference 2024"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total": 5,
        "pages": 1,
        "has_next": false,
        "has_prev": false
    }
}
```

#### Error Responses
- **400 Bad Request**: Invalid status parameter
- **401 Unauthorized**: Invalid or missing JWT token
- **500 Internal Server Error**: Server error

### 3. Cancel Booking
**POST** `/api/bookings/cancel/{booking_id}`

Cancel a booking for the authenticated user.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `booking_id` | integer | Booking ID to cancel |

#### Response (200 OK)
```json
{
    "message": "Booking cancelled successfully",
    "booking": {
        "id": 1,
        "user_id": 2,
        "session_id": 1,
        "status": "cancelled",
        "timestamp": "2024-01-15T10:00:00",
        "created_at": "2024-01-15T09:30:00",
        "updated_at": "2024-01-15T11:00:00",
        "user_name": "John Doe",
        "user_email": "john@example.com",
        "session_time": "2024-01-15T14:00:00",
        "session_location": "Main Conference Hall",
        "event_title": "Tech Conference 2024"
    }
}
```

#### Error Responses
- **400 Bad Request**: Booking already cancelled, session has already passed
- **403 Forbidden**: Booking does not belong to the user
- **404 Not Found**: Booking not found
- **401 Unauthorized**: Invalid or missing JWT token
- **500 Internal Server Error**: Server error

### 4. Reactivate Booking
**POST** `/api/bookings/reactivate/{booking_id}`

Reactivate a cancelled booking for the authenticated user.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `booking_id` | integer | Booking ID to reactivate |

#### Response (200 OK)
```json
{
    "message": "Booking reactivated successfully",
    "booking": {
        "id": 1,
        "user_id": 2,
        "session_id": 1,
        "status": "booked",
        "timestamp": "2024-01-15T10:00:00",
        "created_at": "2024-01-15T09:30:00",
        "updated_at": "2024-01-15T12:00:00",
        "user_name": "John Doe",
        "user_email": "john@example.com",
        "session_time": "2024-01-15T14:00:00",
        "session_location": "Main Conference Hall",
        "event_title": "Tech Conference 2024"
    }
}
```

#### Error Responses
- **400 Bad Request**: Booking already active, session has already passed
- **403 Forbidden**: Booking does not belong to the user
- **404 Not Found**: Booking not found
- **409 Conflict**: User already has an active booking for this session
- **401 Unauthorized**: Invalid or missing JWT token
- **500 Internal Server Error**: Server error

### 5. Get Specific Booking
**GET** `/api/bookings/{booking_id}`

Get a specific booking for the authenticated user.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `booking_id` | integer | Booking ID |

#### Response (200 OK)
```json
{
    "id": 1,
    "user_id": 2,
    "session_id": 1,
    "status": "booked",
    "timestamp": "2024-01-15T10:00:00",
    "created_at": "2024-01-15T09:30:00",
    "updated_at": "2024-01-15T09:30:00",
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "session_time": "2024-01-15T14:00:00",
    "session_location": "Main Conference Hall",
    "event_title": "Tech Conference 2024"
}
```

#### Error Responses
- **403 Forbidden**: Booking does not belong to the user
- **404 Not Found**: Booking not found
- **401 Unauthorized**: Invalid or missing JWT token
- **500 Internal Server Error**: Server error

## Business Logic

### Booking Rules
1. **One Active Booking Per Session**: Users can only have one active booking per session
2. **Past Session Prevention**: Cannot book or cancel bookings for sessions that have already passed
3. **Ownership Validation**: Users can only manage their own bookings
4. **Automatic Reactivation**: If a user tries to book a session they previously cancelled, the booking is reactivated

### Status Management
- **booked**: Active booking
- **cancelled**: Cancelled booking (can be reactivated)

## Usage Examples

### Using curl

#### Book a session:
```bash
curl -X POST http://localhost:5000/api/bookings/book \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1
  }'
```

#### Get my bookings:
```bash
curl -X GET "http://localhost:5000/api/bookings/my-bookings?status=booked" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Cancel a booking:
```bash
curl -X POST http://localhost:5000/api/bookings/cancel/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Reactivate a booking:
```bash
curl -X POST http://localhost:5000/api/bookings/reactivate/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Using Python requests

```python
import requests

# Set up headers with JWT token
headers = {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
}

# Book a session
response = requests.post('http://localhost:5000/api/bookings/book', 
                        json={'session_id': 1}, 
                        headers=headers)
if response.status_code == 201:
    booking = response.json()['booking']
    print(f"Booked session: {booking['session_location']}")

# Get my bookings
response = requests.get('http://localhost:5000/api/bookings/my-bookings', 
                       headers=headers)
if response.status_code == 200:
    bookings = response.json()['bookings']
    for booking in bookings:
        print(f"Booking: {booking['event_title']} - {booking['status']}")

# Cancel a booking
response = requests.post('http://localhost:5000/api/bookings/cancel/1', 
                        headers=headers)
if response.status_code == 200:
    print("Booking cancelled successfully")
```

### Using JavaScript fetch

```javascript
// Set up headers with JWT token
const headers = {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
};

// Book a session
fetch('/api/bookings/book', {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({ session_id: 1 })
})
.then(response => response.json())
.then(data => {
    console.log('Booking created:', data.booking);
});

// Get my bookings
fetch('/api/bookings/my-bookings?status=booked', {
    headers: { 'Authorization': 'Bearer YOUR_JWT_TOKEN' }
})
.then(response => response.json())
.then(data => {
    console.log('My bookings:', data.bookings);
});

// Cancel a booking
fetch('/api/bookings/cancel/1', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer YOUR_JWT_TOKEN' }
})
.then(response => response.json())
.then(data => {
    console.log('Booking cancelled:', data.message);
});
```

## Error Handling

### Common Error Responses

#### 401 Unauthorized
```json
{
    "error": "Missing Authorization Header"
}
```

#### 403 Forbidden
```json
{
    "error": "You can only cancel your own bookings"
}
```

#### 404 Not Found
```json
{
    "error": "Session not found"
}
```

#### 409 Conflict
```json
{
    "error": "You already have an active booking for this session"
}
```

## Testing

Run the test script to verify the endpoints work correctly:

```bash
python test_booking_routes.py
```

This will test all endpoints with authentication and various scenarios.

## Database Requirements

Make sure the database has the following tables:
- `bookings` - Booking information
- `sessions` - Session information
- `users` - User information
- `events` - Event information

Run migrations if needed:
```bash
flask db upgrade
```

## Security Features

1. **JWT Authentication**: All endpoints require valid JWT tokens
2. **User Ownership**: Users can only access their own bookings
3. **Input Validation**: Comprehensive validation of all inputs
4. **Business Logic Validation**: Prevents invalid operations (e.g., booking past sessions)
5. **Error Handling**: Proper error responses without exposing sensitive information 