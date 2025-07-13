# Booking Model Documentation

This document describes the Booking model and its relationships with other models in the application.

## Overview

The Booking model represents user reservations for sessions within events. It tracks the relationship between users and sessions, including booking status and timestamps.

## Booking Model

### Table: `bookings`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key | Unique identifier |
| `user_id` | Integer | Foreign Key, Not Null | Reference to users.id |
| `session_id` | Integer | Foreign Key, Not Null | Reference to sessions.id |
| `status` | String(20) | Not Null, Default: 'booked' | Booking status |
| `timestamp` | DateTime | Auto | Booking timestamp |
| `created_at` | DateTime | Auto | Creation timestamp |
| `updated_at` | DateTime | Auto | Last update timestamp |

### Relationships

- **Many-to-One**: Multiple Bookings belong to one User
- **Many-to-One**: Multiple Bookings belong to one Session
- **Backrefs**: 
  - `user` - Access the user who made the booking
  - `session` - Access the session being booked

## BookingStatus Enum

The model uses an enum to ensure consistent status values:

```python
class BookingStatus(Enum):
    BOOKED = "booked"
    CANCELLED = "cancelled"
```

## Properties

### `is_active`
Returns `True` if the booking status is 'booked' (not cancelled).

### `is_cancelled`
Returns `True` if the booking status is 'cancelled'.

## Methods

### Instance Methods

#### `to_dict()`
Converts the booking to a dictionary representation for JSON serialization.

```python
booking_dict = booking.to_dict()
# Returns:
{
    'id': 1,
    'user_id': 2,
    'session_id': 3,
    'status': 'booked',
    'timestamp': '2024-01-15T10:00:00',
    'created_at': '2024-01-15T09:30:00',
    'updated_at': '2024-01-15T09:30:00',
    'user_name': 'John Doe',
    'user_email': 'john@example.com',
    'session_time': '2024-01-15T14:00:00',
    'session_location': 'Main Conference Hall',
    'event_title': 'Tech Conference 2024'
}
```

#### `cancel()`
Changes the booking status to 'cancelled' and updates the timestamp.

```python
booking.cancel()
# Status becomes 'cancelled'
```

#### `reactivate()`
Changes the booking status back to 'booked' and updates the timestamp.

```python
booking.reactivate()
# Status becomes 'booked'
```

### Class Methods

#### `get_user_bookings(user_id, status=None)`
Get all bookings for a specific user with optional status filter.

```python
# Get all bookings for user 1
bookings = Booking.get_user_bookings(1)

# Get only active bookings for user 1
active_bookings = Booking.get_user_bookings(1, BookingStatus.BOOKED.value)
```

#### `get_session_bookings(session_id, status=None)`
Get all bookings for a specific session with optional status filter.

```python
# Get all bookings for session 1
bookings = Booking.get_session_bookings(1)

# Get only cancelled bookings for session 1
cancelled_bookings = Booking.get_session_bookings(1, BookingStatus.CANCELLED.value)
```

#### `get_active_bookings(session_id)`
Get all active (booked) bookings for a session.

```python
active_bookings = Booking.get_active_bookings(1)
```

#### `count_session_bookings(session_id, status=None)`
Count bookings for a session with optional status filter.

```python
# Count all bookings for session 1
total_bookings = Booking.count_session_bookings(1)

# Count only active bookings for session 1
active_count = Booking.count_session_bookings(1, BookingStatus.BOOKED.value)
```

#### `user_has_booking_for_session(user_id, session_id)`
Check if a user has an active booking for a specific session.

```python
has_booking = Booking.user_has_booking_for_session(1, 2)
# Returns True if user 1 has an active booking for session 2
```

## Database Relationships

```
User (1) ←→ (Many) Booking ←→ (Many) Session (1)
```

- A User can have multiple Bookings
- A Session can have multiple Bookings
- A Booking belongs to exactly one User and one Session

## Usage Examples

### Creating a Booking

```python
from main_app.models import Booking, BookingStatus

# Create a new booking
booking = Booking()
booking.user_id = user.id
booking.session_id = session.id
booking.status = BookingStatus.BOOKED.value

# Save to database
db.session.add(booking)
db.session.commit()
```

### Managing Booking Status

```python
# Cancel a booking
booking.cancel()
db.session.commit()

# Reactivate a cancelled booking
booking.reactivate()
db.session.commit()

# Check booking status
if booking.is_active:
    print("Booking is active")
elif booking.is_cancelled:
    print("Booking is cancelled")
```

### Querying Bookings

```python
# Get all bookings for a user
user_bookings = Booking.get_user_bookings(user.id)

# Get active bookings for a session
active_bookings = Booking.get_active_bookings(session.id)

# Check if user has booking for session
if Booking.user_has_booking_for_session(user.id, session.id):
    print("User already has a booking for this session")

# Count bookings for a session
booking_count = Booking.count_session_bookings(session.id)
```

### Working with Related Data

```python
# Get booking with user and session details
booking = Booking.query.get(1)

# Access user information
user_name = booking.user.name
user_email = booking.user.email

# Access session information
session_time = booking.session.time
session_location = booking.session.location
event_title = booking.session.event.title

# Get all bookings for a user with session details
user_bookings = Booking.query.filter_by(user_id=user.id).all()
for booking in user_bookings:
    print(f"Booked: {booking.session.event.title} - {booking.session.location}")
```

## Validation Rules

### Booking Validation
- `user_id` must reference a valid user
- `session_id` must reference a valid session
- `status` must be either 'booked' or 'cancelled'
- A user cannot have multiple active bookings for the same session

### Business Logic
- Only one active booking per user per session
- Cancelled bookings can be reactivated
- Booking timestamps are automatically set

## Best Practices

1. **Status Management**: Use the provided methods (`cancel()`, `reactivate()`) instead of directly setting status
2. **Duplicate Prevention**: Check for existing bookings before creating new ones
3. **Data Integrity**: Use foreign key constraints to ensure data consistency
4. **Audit Trail**: The `created_at` and `updated_at` fields provide audit information
5. **Performance**: Use class methods for common queries to optimize database access

## Integration with Other Models

### User Model
```python
# Access user's bookings
user = User.query.get(1)
for booking in user.bookings:
    print(f"Booked session: {booking.session.event.title}")
```

### Session Model
```python
# Access session's bookings
session = Session.query.get(1)
for booking in session.bookings:
    print(f"Booked by: {booking.user.name}")
```

### Event Model
```python
# Get all bookings for an event
event = Event.query.get(1)
all_bookings = []
for session in event.sessions:
    all_bookings.extend(session.bookings)
```

## Database Migrations

After creating this model, you'll need to create and run database migrations:

```bash
# Create migration
flask db migrate -m "Add Booking model"

# Apply migration
flask db upgrade
```

## Testing

Run the test script to verify the model works correctly:

```bash
python test_booking_model.py
```

This will test model creation, properties, methods, and relationships.

## Common Use Cases

1. **Session Registration**: Users book sessions for events
2. **Capacity Management**: Track how many people are booked for each session
3. **User Dashboard**: Show users their upcoming and past bookings
4. **Cancellation Management**: Allow users to cancel and reactivate bookings
5. **Reporting**: Generate reports on session popularity and attendance 