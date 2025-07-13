# Event Routes API Documentation

This document describes the Event and Session API endpoints available in the Flask application.

## Base URL
All event and session endpoints are prefixed with `/api`

## Endpoints

### 1. Get All Events
**GET** `/api/events`

Retrieve a paginated list of all events with optional filtering.

#### Query Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `page` | integer | Page number for pagination | 1 |
| `per_page` | integer | Number of events per page | 10 |
| `status` | string | Filter by event status: `upcoming`, `active`, `past` | None |
| `search` | string | Search in title and description | None |

#### Response (200 OK)
```json
{
    "events": [
        {
            "id": 1,
            "title": "Tech Conference 2024",
            "description": "Annual technology conference",
            "start_date": "2024-01-15T09:00:00",
            "end_date": "2024-01-17T18:00:00",
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00",
            "sessions_count": 5
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total": 25,
        "pages": 3,
        "has_next": true,
        "has_prev": false
    }
}
```

#### Example Requests
```bash
# Get all events
curl -X GET "http://localhost:5000/api/events"

# Get upcoming events only
curl -X GET "http://localhost:5000/api/events?status=upcoming"

# Search for events containing "conference"
curl -X GET "http://localhost:5000/api/events?search=conference"

# Get events with pagination
curl -X GET "http://localhost:5000/api/events?page=2&per_page=5"
```

### 2. Get All Sessions
**GET** `/api/sessions`

Retrieve a paginated list of all sessions with optional filtering.

#### Query Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `page` | integer | Page number for pagination | 1 |
| `per_page` | integer | Number of sessions per page | 10 |
| `event_id` | integer | Filter by event ID | None |
| `facilitator_id` | integer | Filter by facilitator ID | None |
| `status` | string | Filter by session status: `upcoming`, `ongoing`, `past` | None |
| `location` | string | Filter by location (partial match) | None |

#### Response (200 OK)
```json
{
    "sessions": [
        {
            "id": 1,
            "event_id": 1,
            "facilitator_id": 2,
            "time": "2024-01-15T10:00:00",
            "location": "Main Conference Hall",
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00",
            "facilitator_name": "John Doe",
            "event_title": "Tech Conference 2024"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total": 15,
        "pages": 2,
        "has_next": true,
        "has_prev": false
    }
}
```

#### Example Requests
```bash
# Get all sessions
curl -X GET "http://localhost:5000/api/sessions"

# Get sessions for a specific event
curl -X GET "http://localhost:5000/api/sessions?event_id=1"

# Get sessions by a specific facilitator
curl -X GET "http://localhost:5000/api/sessions?facilitator_id=2"

# Get upcoming sessions
curl -X GET "http://localhost:5000/api/sessions?status=upcoming"

# Get sessions in a specific location
curl -X GET "http://localhost:5000/api/sessions?location=hall"
```

### 3. Get Specific Event
**GET** `/api/events/{event_id}`

Retrieve a specific event by ID with all its sessions.

#### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `event_id` | integer | Event ID |

#### Response (200 OK)
```json
{
    "id": 1,
    "title": "Tech Conference 2024",
    "description": "Annual technology conference",
    "start_date": "2024-01-15T09:00:00",
    "end_date": "2024-01-17T18:00:00",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00",
    "sessions_count": 3,
    "sessions": [
        {
            "id": 1,
            "event_id": 1,
            "facilitator_id": 2,
            "time": "2024-01-15T10:00:00",
            "location": "Main Conference Hall",
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00",
            "facilitator_name": "John Doe",
            "event_title": "Tech Conference 2024"
        }
    ]
}
```

#### Error Responses
- **404 Not Found**: Event not found

#### Example Request
```bash
curl -X GET "http://localhost:5000/api/events/1"
```

### 4. Get Specific Session
**GET** `/api/sessions/{session_id}`

Retrieve a specific session by ID.

#### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `session_id` | integer | Session ID |

#### Response (200 OK)
```json
{
    "id": 1,
    "event_id": 1,
    "facilitator_id": 2,
    "time": "2024-01-15T10:00:00",
    "location": "Main Conference Hall",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00",
    "facilitator_name": "John Doe",
    "event_title": "Tech Conference 2024"
}
```

#### Error Responses
- **404 Not Found**: Session not found

#### Example Request
```bash
curl -X GET "http://localhost:5000/api/sessions/1"
```

## Filtering Options

### Event Status Filters
- `upcoming`: Events that haven't started yet
- `active`: Events currently ongoing
- `past`: Events that have ended

### Session Status Filters
- `upcoming`: Sessions that haven't started yet
- `ongoing`: Sessions currently ongoing (within 2 hours of start time)
- `past`: Sessions that have ended

### Search Functionality
- Events can be searched by title and description
- Sessions can be filtered by location (partial match)
- Search is case-insensitive

## Pagination

All list endpoints support pagination with the following response structure:

```json
{
    "pagination": {
        "page": 1,           // Current page number
        "per_page": 10,      // Items per page
        "total": 25,         // Total number of items
        "pages": 3,          // Total number of pages
        "has_next": true,    // Whether there's a next page
        "has_prev": false    // Whether there's a previous page
    }
}
```

## Error Handling

### Common Error Responses

#### 404 Not Found
```json
{
    "error": "Event not found"
}
```

#### 500 Internal Server Error
```json
{
    "error": "Internal server error"
}
```

## Usage Examples

### Using Python requests

```python
import requests

# Get all events
response = requests.get('http://localhost:5000/api/events')
events = response.json()

# Get upcoming events
response = requests.get('http://localhost:5000/api/events?status=upcoming')
upcoming_events = response.json()

# Get sessions for a specific event
response = requests.get('http://localhost:5000/api/sessions?event_id=1')
event_sessions = response.json()

# Get a specific event with its sessions
response = requests.get('http://localhost:5000/api/events/1')
event_details = response.json()
```

### Using JavaScript fetch

```javascript
// Get all events
fetch('/api/events')
    .then(response => response.json())
    .then(data => {
        console.log('Events:', data.events);
        console.log('Pagination:', data.pagination);
    });

// Get upcoming events
fetch('/api/events?status=upcoming')
    .then(response => response.json())
    .then(data => {
        console.log('Upcoming events:', data.events);
    });

// Get sessions for an event
fetch('/api/sessions?event_id=1')
    .then(response => response.json())
    .then(data => {
        console.log('Event sessions:', data.sessions);
    });
```

## Performance Considerations

1. **Pagination**: Always use pagination for large datasets
2. **Filtering**: Use filters to reduce data transfer
3. **Indexing**: Ensure database indexes on frequently filtered fields
4. **Caching**: Consider caching for frequently accessed data

## Testing

Run the test script to verify the endpoints work correctly:

```bash
python test_event_routes.py
```

This will test all endpoints with various filters and error conditions.

## Database Requirements

Make sure the database has the following tables:
- `events` - Event information
- `sessions` - Session information
- `users` - User information (for facilitators)

Run migrations if needed:
```bash
flask db upgrade
``` 