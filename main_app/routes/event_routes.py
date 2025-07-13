from flask import Blueprint, jsonify, request
from main_app.models import db
from main_app.models.event import Event
from main_app.models.session import Session
from main_app.models.booking import Booking, BookingStatus
from datetime import datetime
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, get_jwt_identity

event_bp = Blueprint('events', __name__)

@event_bp.route('/events', methods=['GET'])
def get_events():
    """Get all events with optional filtering and pagination"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', type=str)  # upcoming, active, past
        search = request.args.get('search', type=str)
        
        # Build query
        query = Event.query
        
        # Apply status filter
        if status:
            now = datetime.utcnow()
            if status == 'upcoming':
                query = query.filter(Event.start_date > now)
            elif status == 'active':
                query = query.filter(Event.start_date <= now, Event.end_date >= now)
            elif status == 'past':
                query = query.filter(Event.end_date < now)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Event.title.ilike(search_term)) |
                (Event.description.ilike(search_term))
            )
        
        # Order by start date (newest first)
        query = query.order_by(desc(Event.start_date))
        
        # Apply pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        events = pagination.items
        
        # Convert to dictionary format
        events_data = []
        for event in events:
            event_dict = event.to_dict()
            # Add sessions count
            event_dict['sessions_count'] = len(event.sessions) if event.sessions else 0
            events_data.append(event_dict)
        
        return jsonify({
            'events': events_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@event_bp.route('/dashboard/events', methods=['GET'])
@jwt_required()
def get_user_dashboard_events():
    """Get all events for user dashboard with booking information"""
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', type=str)  # upcoming, active, past
        search = request.args.get('search', type=str)
        
        # Build query
        query = Event.query
        
        # Apply status filter
        if status:
            now = datetime.utcnow()
            if status == 'upcoming':
                query = query.filter(Event.start_date > now)
            elif status == 'active':
                query = query.filter(Event.start_date <= now, Event.end_date >= now)
            elif status == 'past':
                query = query.filter(Event.end_date < now)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Event.title.ilike(search_term)) |
                (Event.description.ilike(search_term))
            )
        
        # Order by start date (newest first)
        query = query.order_by(desc(Event.start_date))
        
        # Apply pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        events = pagination.items
        
        # Convert to dictionary format with user-specific information
        events_data = []
        for event in events:
            event_dict = event.to_dict()
            
            # Add sessions count
            event_dict['sessions_count'] = len(event.sessions) if event.sessions else 0
            
            # Add user's booking information for this event
            user_bookings = []
            if event.sessions:
                for session in event.sessions:
                    booking = Booking.query.filter_by(
                        user_id=current_user_id,
                        session_id=session.id
                    ).first()
                    
                    if booking:
                        user_bookings.append({
                            'session_id': session.id,
                            'session_time': session.time.isoformat() if session.time else None,
                            'session_location': session.location,
                            'booking_status': booking.status,
                            'booking_id': booking.id
                        })
            
            event_dict['user_bookings'] = user_bookings
            event_dict['has_user_bookings'] = len(user_bookings) > 0
            
            # Add event status for better UX
            now = datetime.utcnow()
            if event.start_date > now:
                event_dict['status'] = 'upcoming'
            elif event.start_date <= now <= event.end_date:
                event_dict['status'] = 'active'
            else:
                event_dict['status'] = 'past'
            
            events_data.append(event_dict)
        
        return jsonify({
            'events': events_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'user_id': current_user_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@event_bp.route('/sessions', methods=['GET'])
def get_sessions():
    """Get all sessions with optional filtering and pagination"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        event_id = request.args.get('event_id', type=int)
        facilitator_id = request.args.get('facilitator_id', type=int)
        status = request.args.get('status', type=str)  # upcoming, ongoing, past
        location = request.args.get('location', type=str)
        
        # Build query
        query = Session.query
        
        # Apply filters
        if event_id:
            query = query.filter(Session.event_id == event_id)
        
        if facilitator_id:
            query = query.filter(Session.facilitator_id == facilitator_id)
        
        if location:
            location_term = f"%{location}%"
            query = query.filter(Session.location.ilike(location_term))
        
        # Apply status filter
        if status:
            now = datetime.utcnow()
            if status == 'upcoming':
                query = query.filter(Session.time > now)
            elif status == 'ongoing':
                # Sessions are ongoing if within 2 hours of start time
                from datetime import timedelta
                session_end = Session.time + timedelta(hours=2)
                query = query.filter(Session.time <= now, session_end >= now)
            elif status == 'past':
                query = query.filter(Session.time < now)
        
        # Order by time (newest first)
        query = query.order_by(desc(Session.time))
        
        # Apply pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        sessions = pagination.items
        
        # Convert to dictionary format
        sessions_data = []
        for session in sessions:
            session_dict = session.to_dict()
            sessions_data.append(session_dict)
        
        return jsonify({
            'sessions': sessions_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@event_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get a specific event by ID with its sessions"""
    try:
        event = Event.query.get_or_404(event_id)
        
        # Get event data
        event_data = event.to_dict()
        
        # Get sessions for this event
        sessions = Session.query.filter_by(event_id=event_id).order_by(Session.time).all()
        sessions_data = [session.to_dict() for session in sessions]
        
        event_data['sessions'] = sessions_data
        event_data['sessions_count'] = len(sessions_data)
        
        return jsonify(event_data), 200
        
    except Exception as e:
        return jsonify({'error': 'Event not found'}), 404

@event_bp.route('/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    """Get a specific session by ID"""
    try:
        session = Session.query.get_or_404(session_id)
        return jsonify(session.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': 'Session not found'}), 404

@event_bp.route('/events/<int:event_id>/sessions', methods=['GET'])
@jwt_required()
def get_event_sessions(event_id):
    event = Event.query.get_or_404(event_id)
    sessions = event.sessions
    return jsonify({
        'sessions': [s.to_dict() for s in sessions]
    }), 200
