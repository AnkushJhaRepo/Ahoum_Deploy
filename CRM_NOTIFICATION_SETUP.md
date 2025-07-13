# CRM Notification System Setup

This document explains how to set up and use the CRM notification system that notifies facilitators when sessions are booked.

## Overview

The CRM notification system consists of two components:

1. **Main Flask Application** (Port 5000) - Handles user authentication, event management, and session booking
2. **CRM Microservice** (Port 5001) - Receives and stores booking notifications for facilitators

## Features

- ✅ Automatic notifications when sessions are booked
- ✅ Notifications when bookings are reactivated
- ✅ Detailed booking information including user, event, and facilitator details
- ✅ Persistent storage of notifications
- ✅ Comprehensive logging
- ✅ RESTful API for notification management

## Quick Start

### 1. Start Both Services

Use the provided script to start both services simultaneously:

```bash
python start_services.py
```

This will:
- Start the CRM microservice on port 5001
- Start the main Flask app on port 5000
- Display service URLs and testing instructions

### 2. Manual Service Start

If you prefer to start services manually:

#### Start CRM Microservice:
```bash
cd crm_microservice
python crm_app.py
```

#### Start Main Flask App (in another terminal):
```bash
python main_app/app.py
```

### 3. Test the System

#### Option A: Use the Test Script
```bash
python test_crm_booking_notification.py
```

#### Option B: Manual Testing
1. Open http://localhost:5000 in your browser
2. Register a new user or login
3. Browse events and book a session
4. Check notifications at http://localhost:5001/notifications

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# CRM Service Configuration
CRM_BASE_URL=http://localhost:5001
CRM_AUTH_TOKEN=your-secret-token-here

# Main App Configuration
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

### Default Values

If no environment variables are set, the system uses these defaults:

- **CRM_BASE_URL**: `http://localhost:5001`
- **CRM_AUTH_TOKEN**: `your-static-bearer-token-here`
- **CRM_PORT**: `5001`
- **NOTIFICATION_LOG_FILE**: `notifications.json`

## API Endpoints

### CRM Microservice (Port 5001)

#### Health Check
```http
GET /health
```

#### Send Notification
```http
POST /notify
Authorization: Bearer your-static-bearer-token-here
Content-Type: application/json

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

#### Get Notifications
```http
GET /notifications
```

### Main App (Port 5000)

#### Book Session
```http
POST /bookings/book
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
    "session_id": 123
}
```

## How It Works

### 1. Session Booking Flow

1. User authenticates and books a session via the frontend or API
2. Main app creates a booking record in the database
3. Main app automatically sends a notification to the CRM service
4. CRM service validates the notification and stores it
5. Facilitator can view notifications via CRM dashboard

### 2. Notification Data

Each notification includes:
- **Booking ID**: Unique identifier for the booking
- **User Information**: Name, email, and user ID
- **Event Information**: Event title, ID, and start date
- **Facilitator ID**: ID of the session facilitator
- **Timestamp**: When the notification was received

### 3. Error Handling

- If CRM service is unavailable, booking still succeeds
- Failed notifications are logged but don't affect booking operations
- Automatic retry mechanisms for transient failures

## Testing

### Automated Testing

Run the comprehensive test suite:

```bash
python test_crm_booking_notification.py
```

This test:
1. Verifies CRM service connectivity
2. Tests user authentication
3. Books a session and verifies notification
4. Checks notification storage

### Manual Testing

#### Test CRM Service Health:
```bash
curl http://localhost:5001/health
```

#### Test Notification Sending:
```bash
curl -X POST http://localhost:5001/notify \
  -H "Authorization: Bearer your-static-bearer-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 123,
    "user": {
        "id": 456,
        "name": "Test User",
        "email": "test@example.com"
    },
    "event": {
        "id": 789,
        "title": "Test Event",
        "start_date": "2024-01-15T09:00:00"
    },
    "facilitator_id": 101
  }'
```

#### View Stored Notifications:
```bash
curl http://localhost:5001/notifications
```

## Troubleshooting

### Common Issues

#### 1. CRM Service Not Starting
- Check if port 5001 is available
- Verify Python dependencies are installed
- Check logs in `crm_microservice/crm_notifications.log`

#### 2. Notifications Not Being Sent
- Verify CRM service is running on port 5001
- Check authentication token matches between services
- Review main app logs for notification errors

#### 3. Authentication Errors
- Ensure `CRM_AUTH_TOKEN` is set correctly
- Verify token format in Authorization header
- Check token matches between main app and CRM service

### Log Files

- **CRM Service**: `crm_microservice/crm_notifications.log`
- **Main App**: Check console output or Flask logs
- **Notifications**: `crm_microservice/notifications.json`

### Debug Mode

Enable debug mode for more detailed logging:

```bash
# For CRM service
export CRM_DEBUG=true
python crm_microservice/crm_app.py

# For main app
export FLASK_DEBUG=1
python main_app/app.py
```

## Integration with Frontend

The frontend automatically triggers notifications when users book sessions. The process is transparent to users:

1. User clicks "Book Session" button
2. Frontend sends booking request to main app
3. Main app creates booking and sends CRM notification
4. User sees booking confirmation
5. Facilitator receives notification in CRM system

## Security Considerations

- All notifications use Bearer token authentication
- Sensitive data is not logged in plain text
- Failed authentication attempts are logged
- Notifications are stored locally (consider encryption for production)

## Production Deployment

For production deployment:

1. **Use HTTPS**: Configure SSL certificates for both services
2. **Secure Tokens**: Use strong, unique authentication tokens
3. **Database Storage**: Consider using a database instead of JSON files
4. **Monitoring**: Implement health checks and monitoring
5. **Backup**: Regular backup of notification data
6. **Rate Limiting**: Implement rate limiting for notification endpoints

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review log files for error details
3. Verify service configurations
4. Test with the provided test scripts 