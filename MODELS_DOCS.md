# Event and Session Models Documentation

This document describes the Event and Session models and their relationships.

## Overview

The application includes two main models for managing events and sessions:

- **Event**: Represents a main event with title, description, and date range
- **Session**: Represents individual sessions within an event, with facilitators and locations

## Event Model

### Table: `events`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key | Unique identifier |
| `title` | String(200) | Not Null | Event title |
| `description` | Text | Nullable | Event description |
| `start_date` | DateTime | Not Null | Event start date and time |
| `end_date` | DateTime | Not Null | Event end date and time |
| `created_at` | DateTime | Auto | Creation timestamp |
| `updated_at` | DateTime | Auto | Last update timestamp |

### Relationships

- **One-to-Many**: One Event can have multiple Sessions
- **Backref**: `event` - Access the parent event from a session

### Properties

#### `is_active`
Returns `True` if the event is currently ongoing (current time is between start_date and end_date).

#### `is_upcoming`
Returns `True` if the event hasn't started yet (current time is before start_date).

#### `is_past`
Returns `True` if the event has ended (current time is after end_date).

### Methods

#### `to_dict()`
Converts the event to a dictionary representation for JSON serialization.

```python
event_dict = event.to_dict()
# Returns:
{
    'id': 1,
    'title': 'Tech Conference 2024',
    'description': 'Annual technology conference',
    'start_date': '2024-01-15T09:00:00',
    'end_date': '2024-01-17T18:00:00',
    'created_at': '2024-01-01T10:00:00',
    'updated_at': '2024-01-01T10:00:00',
    'sessions_count': 0
}
```

## Session Model

### Table: `sessions`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key | Unique identifier |
| `event_id` | Integer | Foreign Key, Not Null | Reference to events.id |
| `facilitator_id` | Integer | Foreign Key, Not Null | Reference to users.id |
| `time` | DateTime | Not Null | Session start time |
| `location` | String(200) | Not Null | Session location |
| `created_at` | DateTime | Auto | Creation timestamp |
| `updated_at` | DateTime | Auto | Last update timestamp |

### Relationships

- **Many-to-One**: Multiple Sessions belong to one Event
- **Many-to-One**: Multiple Sessions can be facilitated by one User
- **Backrefs**: 
  - `event` - Access the parent event
  - `facilitator` - Access the session facilitator (User)

### Properties

#### `is_upcoming`
Returns `True` if the session hasn't started yet (current time is before session time).

#### `is_past`
Returns `True` if the session has ended (current time is after session time).

#### `is_ongoing`
Returns `True` if the session is currently ongoing (within 2 hours of start time).

### Methods

#### `to_dict()`
Converts the session to a dictionary representation for JSON serialization.

```python
session_dict = session.to_dict()
# Returns:
{
    'id': 1,
    'event_id': 1,
    'facilitator_id': 2,
    'time': '2024-01-15T10:00:00',
    'location': 'Main Conference Hall',
    'created_at': '2024-01-01T10:00:00',
    'updated_at': '2024-01-01T10:00:00',
    'facilitator_name': 'John Doe',
    'event_title': 'Tech Conference 2024'
}
```

## Database Relationships

```
User (1) ←→ (Many) Session ←→ (Many) Event (1)
```

- A User can facilitate multiple Sessions
- A Session belongs to one Event
- An Event can have multiple Sessions

## Usage Examples

### Creating an Event

```python
from main_app.models import Event
from datetime import datetime, timedelta

# Create a new event
event = Event()
event.title = "Annual Tech Conference"
event.description = "Join us for the biggest tech event of the year"
event.start_date = datetime.utcnow() + timedelta(days=30)
event.end_date = datetime.utcnow() + timedelta(days=32)

# Save to database
db.session.add(event)
db.session.commit()
```

### Creating a Session

```python
from main_app.models import Session

# Create a new session
session = Session()
session.event_id = event.id
session.facilitator_id = user.id
session.time = datetime.utcnow() + timedelta(days=30, hours=2)
session.location = "Main Conference Hall"

# Save to database
db.session.add(session)
db.session.commit()
```

### Querying Events and Sessions

```python
# Get all upcoming events
upcoming_events = Event.query.filter(Event.start_date > datetime.utcnow()).all()

# Get all sessions for an event
event_sessions = Session.query.filter_by(event_id=event.id).all()

# Get all sessions facilitated by a user
user_sessions = Session.query.filter_by(facilitator_id=user.id).all()

# Get event with its sessions
event_with_sessions = Event.query.get(event.id)
for session in event_with_sessions.sessions:
    print(f"Session: {session.location} at {session.time}")
```

### Using Model Properties

```python
# Check event status
if event.is_upcoming:
    print("Event hasn't started yet")
elif event.is_active:
    print("Event is currently ongoing")
elif event.is_past:
    print("Event has ended")

# Check session status
if session.is_upcoming:
    print("Session hasn't started yet")
elif session.is_ongoing:
    print("Session is currently ongoing")
elif session.is_past:
    print("Session has ended")
```

## Database Migrations

After creating these models, you'll need to create and run database migrations:

```bash
# Create migration
flask db migrate -m "Add Event and Session models"

# Apply migration
flask db upgrade
```

## Validation Rules

### Event Validation
- `title` is required and must be a string
- `start_date` and `end_date` are required and must be datetime objects
- `end_date` should be after `start_date` (application-level validation recommended)

### Session Validation
- `event_id` must reference a valid event
- `facilitator_id` must reference a valid user
- `time` is required and must be a datetime object
- `location` is required and must be a string

## Best Practices

1. **Date Validation**: Always validate that end_date is after start_date
2. **Time Zones**: Consider timezone handling for production applications
3. **Cascade Deletes**: Sessions are automatically deleted when their parent event is deleted
4. **Indexing**: Consider adding indexes on frequently queried fields like `start_date`, `time`, etc.
5. **Soft Deletes**: Consider implementing soft deletes for production applications

## Testing

Run the test script to verify the models work correctly:

```bash
python test_models.py
```

This will test model creation, properties, methods, and relationships. 