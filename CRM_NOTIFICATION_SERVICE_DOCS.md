# CRM Notification Service Documentation

## Overview

The `CRMNotificationService` is a service class that handles communication between the main Flask application and the CRM microservice. It provides methods to send various types of notifications to the CRM service for tracking and processing.

## Features

- **Authentication**: Uses Bearer token authentication for secure communication
- **Error Handling**: Comprehensive error handling with detailed logging
- **Timeout Management**: Configurable timeout for HTTP requests
- **Flexible Payloads**: Support for custom notification types and additional data
- **Connection Testing**: Built-in health check functionality
- **Specialized Methods**: Pre-built methods for common notification types

## Configuration

### Environment Variables

Add these to your `.env` file or Flask configuration:

```bash
CRM_BASE_URL=http://localhost:5001
CRM_AUTH_TOKEN=your-secret-token
```

### Default Values

- **Base URL**: `http://localhost:5001`
- **Auth Token**: `your-secret-token`
- **Request Timeout**: 10 seconds
- **Health Check Timeout**: 5 seconds

## Usage

### Basic Usage

```python
from main_app.services.notify_crm import CRMNotificationService

# Initialize the service
crm_service = CRMNotificationService()

# Send a general notification
result = crm_service.send_notification(
    notification_type="user_registered",
    user_id=123,
    message="New user registered",
    additional_data={"email": "user@example.com"}
)
```

### Booking Notifications

```python
# Send booking created notification
result = crm_service.send_booking_notification(
    booking_id=456,
    user_id=123,
    session_id=789,
    action="created",
    additional_data={"session_name": "Yoga Class"}
)

# Send booking cancelled notification
result = crm_service.send_booking_notification(
    booking_id=456,
    user_id=123,
    session_id=789,
    action="cancelled"
)
```

### Event Notifications

```python
# Send event created notification
result = crm_service.send_event_notification(
    event_id=101,
    user_id=123,
    action="created",
    additional_data={"event_name": "Summer Festival"}
)

# Send event updated notification
result = crm_service.send_event_notification(
    event_id=101,
    user_id=123,
    action="updated"
)
```

### Connection Testing

```python
# Test if CRM service is accessible
if crm_service.test_connection():
    print("CRM service is available")
else:
    print("CRM service is not accessible")
```

## API Reference

### CRMNotificationService

#### Constructor

```python
CRMNotificationService(base_url: Optional[str] = None, auth_token: Optional[str] = None)
```

**Parameters:**
- `base_url` (str, optional): Base URL of the CRM microservice
- `auth_token` (str, optional): Bearer token for authentication

#### Methods

##### send_notification()

```python
send_notification(
    notification_type: str,
    user_id: int,
    message: str,
    additional_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Sends a general notification to the CRM service.

**Parameters:**
- `notification_type` (str): Type of notification (e.g., 'booking_created', 'user_registered')
- `user_id` (int): ID of the user related to the notification
- `message` (str): Human-readable notification message
- `additional_data` (dict, optional): Additional data to include in the notification

**Returns:**
- `dict`: Response from the CRM service

**Raises:**
- `Exception`: If the request fails

##### send_booking_notification()

```python
send_booking_notification(
    booking_id: int,
    user_id: int,
    session_id: int,
    action: str,
    additional_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Sends a booking-related notification to the CRM service.

**Parameters:**
- `booking_id` (int): ID of the booking
- `user_id` (int): ID of the user
- `session_id` (int): ID of the session
- `action` (str): Action performed (e.g., 'created', 'cancelled', 'reactivated')
- `additional_data` (dict, optional): Additional data to include

**Returns:**
- `dict`: Response from the CRM service

##### send_event_notification()

```python
send_event_notification(
    event_id: int,
    user_id: int,
    action: str,
    additional_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Sends an event-related notification to the CRM service.

**Parameters:**
- `event_id` (int): ID of the event
- `user_id` (int): ID of the user
- `action` (str): Action performed (e.g., 'created', 'updated', 'deleted')
- `additional_data` (dict, optional): Additional data to include

**Returns:**
- `dict`: Response from the CRM service

##### test_connection()

```python
test_connection() -> bool
```

Tests the connection to the CRM microservice.

**Returns:**
- `bool`: True if connection is successful, False otherwise

## Integration Examples

### Integration with Booking Routes

```python
from main_app.services.notify_crm import CRMNotificationService

# In your booking creation route
@app.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    # ... booking creation logic ...
    
    # Send notification to CRM
    try:
        crm_service = CRMNotificationService()
        crm_service.send_booking_notification(
            booking_id=booking.id,
            user_id=current_user.id,
            session_id=booking.session_id,
            action="created",
            additional_data={"session_name": booking.session.name}
        )
    except Exception as e:
        # Log error but don't fail the booking creation
        current_app.logger.error(f"Failed to send CRM notification: {e}")
    
    return jsonify({"message": "Booking created successfully"})
```

### Integration with Event Routes

```python
# In your event creation route
@app.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    # ... event creation logic ...
    
    # Send notification to CRM
    try:
        crm_service = CRMNotificationService()
        crm_service.send_event_notification(
            event_id=event.id,
            user_id=current_user.id,
            action="created",
            additional_data={"event_name": event.name}
        )
    except Exception as e:
        current_app.logger.error(f"Failed to send CRM notification: {e}")
    
    return jsonify({"message": "Event created successfully"})
```

## Error Handling

The service handles various types of errors:

### Network Errors
- **Timeout**: Request takes too long to complete
- **Connection Error**: Cannot connect to CRM service
- **HTTP Error**: CRM service returns an error status code

### Data Errors
- **JSON Decode Error**: Invalid JSON response from CRM service
- **Validation Error**: Invalid data in notification payload

### Logging

All errors are logged with appropriate log levels:
- **INFO**: Successful operations
- **WARNING**: Non-critical issues (e.g., expired tokens)
- **ERROR**: Critical errors that prevent operation

## Testing

### Manual Testing

1. Start the CRM microservice:
   ```bash
   cd crm_microservice
   python crm_app.py
   ```

2. Run the test script:
   ```bash
   python test_notify_crm.py
   ```

### Automated Testing

```python
import unittest
from unittest.mock import patch, Mock
from main_app.services.notify_crm import CRMNotificationService

class TestCRMNotificationService(unittest.TestCase):
    
    def setUp(self):
        self.service = CRMNotificationService()
    
    @patch('requests.post')
    def test_send_notification_success(self, mock_post):
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = self.service.send_notification(
            notification_type="test",
            user_id=1,
            message="Test message"
        )
        
        self.assertEqual(result["status"], "success")
    
    @patch('requests.post')
    def test_send_notification_failure(self, mock_post):
        # Mock failed response
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        with self.assertRaises(Exception):
            self.service.send_notification(
                notification_type="test",
                user_id=1,
                message="Test message"
            )
```

## Security Considerations

1. **Token Management**: Store authentication tokens securely in environment variables
2. **HTTPS**: Use HTTPS in production for secure communication
3. **Input Validation**: Validate all input data before sending to CRM service
4. **Error Handling**: Don't expose sensitive information in error messages
5. **Rate Limiting**: Consider implementing rate limiting for notification requests

## Performance Considerations

1. **Async Processing**: Consider using async/await for non-blocking notifications
2. **Connection Pooling**: Reuse HTTP connections when possible
3. **Timeout Configuration**: Set appropriate timeouts based on network conditions
4. **Error Recovery**: Implement retry logic for transient failures
5. **Monitoring**: Monitor notification success rates and response times

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure CRM microservice is running
   - Check if the port is correct
   - Verify firewall settings

2. **Authentication Failed**
   - Verify the auth token is correct
   - Check if the token format is `Bearer <token>`
   - Ensure the token hasn't expired

3. **Timeout Errors**
   - Increase timeout values if needed
   - Check network connectivity
   - Monitor CRM service performance

4. **Invalid JSON Response**
   - Check CRM service logs for errors
   - Verify the response format
   - Ensure proper error handling in CRM service

### Debug Mode

Enable debug logging to see detailed request/response information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
``` 