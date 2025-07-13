from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from main_app.models import db
from main_app.models.user import User
from main_app.models.session import Session
from main_app.models.booking import Booking, BookingStatus
from main_app.models.event import Event
from datetime import datetime
from sqlalchemy import desc

facilitator_bp = Blueprint('facilitator', __name__)

from functools import wraps

def require_facilitator(f):
    """Decorator to require facilitator role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_facilitator:
            return jsonify({'error': 'Facilitator access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@facilitator_bp.route('/users', methods=['GET'])
@jwt_required()
@require_facilitator
def get_registered_users():
    """Get all registered users (facilitators only)"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '').strip()
        
        # Build query
        query = User.query
        
        # Apply search filter
        if search:
            query = query.filter(
                (User.name.ilike(f'%{search}%')) |
                (User.email.ilike(f'%{search}%'))
            )
        
        # Order by creation date (newest first)
        query = query.order_by(desc(User.created_at))
        
        # Apply pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        users = pagination.items
        
        # Convert to dictionary format (exclude password)
        users_data = []
        for user in users:
            user_dict = user.to_dict()
            users_data.append(user_dict)
        
        return jsonify({
            'users': users_data,
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
        current_app.logger.error(f"Error in get_registered_users: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@facilitator_bp.route('/my-sessions', methods=['GET'])
@jwt_required()
@require_facilitator
def get_my_sessions():
    """Get all sessions for the current facilitator"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get sessions for this facilitator
        query = Session.query.filter_by(facilitator_id=current_user_id)
        
        # Order by time (upcoming first)
        query = query.order_by(Session.time)
        
        # Apply pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        sessions = pagination.items
        
        # Convert to dictionary format with additional info
        sessions_data = []
        for session in sessions:
            session_dict = session.to_dict()
            
            # Add event information
            if session.parent_event:
                session_dict['event'] = {
                    'id': session.parent_event.id,
                    'title': session.parent_event.title,
                    'start_date': session.parent_event.start_date.isoformat(),
                    'end_date': session.parent_event.end_date.isoformat()
                }
            
            # Add booking count
            session_dict['booking_count'] = len([b for b in session.bookings if b.is_active])
            
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
        current_app.logger.error(f"Error in get_my_sessions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@facilitator_bp.route('/sessions/<int:session_id>/bookings', methods=['GET'])
@jwt_required()
@require_facilitator
def get_session_bookings(session_id):
    """Get all bookings for a specific session (facilitator must own the session)"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get the session and verify ownership
        session = Session.query.get_or_404(session_id)
        if session.facilitator_id != current_user_id:
            return jsonify({'error': 'You can only view bookings for your own sessions'}), 403
        
        # Get all bookings for this session
        bookings = Booking.query.filter_by(session_id=session_id).all()
        
        # Convert to dictionary format
        bookings_data = []
        for booking in bookings:
            booking_dict = booking.to_dict()
            bookings_data.append(booking_dict)
        
        return jsonify({
            'session': session.to_dict(),
            'bookings': bookings_data,
            'total_bookings': len(bookings_data)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error in get_session_bookings: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@facilitator_bp.route('/sessions/<int:session_id>', methods=['PUT'])
@jwt_required()
@require_facilitator
def update_session(session_id):
    """Update session details (facilitator must own the session)"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get the session and verify ownership
        session = Session.query.get_or_404(session_id)
        if session.facilitator_id != current_user_id:
            return jsonify({'error': 'You can only modify your own sessions'}), 403
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update allowed fields
        if 'time' in data:
            try:
                new_time = datetime.fromisoformat(data['time'].replace('Z', '+00:00'))
                session.time = new_time
            except ValueError:
                return jsonify({'error': 'Invalid time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
        
        if 'location' in data:
            if not data['location'].strip():
                return jsonify({'error': 'Location cannot be empty'}), 400
            session.location = data['location'].strip()
        
        # Update timestamp
        session.updated_at = datetime.utcnow()
        
        # Save to database
        db.session.commit()
        
        return jsonify({
            'message': 'Session updated successfully',
            'session': session.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in update_session: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@facilitator_bp.route('/sessions/<int:session_id>/cancel', methods=['POST'])
@jwt_required()
@require_facilitator
def cancel_session(session_id):
    """Cancel a session and all its bookings (facilitator must own the session)"""
    try:
        current_user_id = get_jwt_identity()
        # Convert to integer for comparison
        current_user_id = int(current_user_id)
        # Debug print
        print(f"[DEBUG] Cancel attempt: user_id={current_user_id} (type: {type(current_user_id)}), session_id={session_id}")
        # Get the session and verify ownership
        session = Session.query.get_or_404(session_id)
        print(f"[DEBUG] Session {session_id} facilitator_id={session.facilitator_id} (type: {type(session.facilitator_id)})")
        print(f"[DEBUG] Comparison: {session.facilitator_id} != {current_user_id} = {session.facilitator_id != current_user_id}")
        if session.facilitator_id != current_user_id:
            print(f"[DEBUG] 403: session.facilitator_id={session.facilitator_id}, current_user_id={current_user_id}")
            return jsonify({'error': 'You can only cancel your own sessions'}), 403
        
        # Check if session is in the past
        if session.is_past:
            return jsonify({'error': 'Cannot cancel a session that has already passed'}), 400
        
        # Get count of active bookings for this session
        active_bookings_count = Booking.query.filter_by(
            session_id=session_id,
            status=BookingStatus.BOOKED.value
        ).count()
        
        # Delete the session (this will cascade delete all bookings)
        db.session.delete(session)
        db.session.commit()
        
        return jsonify({
            'message': f'Session cancelled successfully. {active_bookings_count} bookings were also cancelled.',
            'cancelled_bookings': active_bookings_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in cancel_session: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@facilitator_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@require_facilitator
def facilitator_dashboard():
    """Get facilitator dashboard data"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get facilitator's sessions
        sessions = Session.query.filter_by(facilitator_id=current_user_id).all()
        
        # Get total users
        total_users = User.query.count()
        
        # Get upcoming sessions
        upcoming_sessions = [s for s in sessions if s.is_upcoming]
        
        # Get total bookings across all sessions
        total_bookings = 0
        for session in sessions:
            total_bookings += len([b for b in session.bookings if b.is_active])
        
        return jsonify({
            'total_users': total_users,
            'total_sessions': len(sessions),
            'upcoming_sessions': len(upcoming_sessions),
            'total_bookings': total_bookings,
            'recent_sessions': [s.to_dict() for s in sessions[:5]]  # Last 5 sessions
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error in facilitator_dashboard: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@facilitator_bp.route('/dashboard-page', methods=['GET'])
def facilitator_dashboard_page():
    """Serve the facilitator dashboard HTML page"""
    try:
        # Read the facilitator dashboard HTML file
        import os
        dashboard_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'facilitator_dashboard.html')
        
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Set proper content type
        from flask import Response
        return Response(html_content, mimetype='text/html')
    except FileNotFoundError:
        return "Facilitator dashboard not found", 404
    except Exception as e:
        current_app.logger.error(f"Error serving facilitator dashboard: {str(e)}")
        return "Internal server error", 500

@facilitator_bp.route('/dashboard.html', methods=['GET'])
def facilitator_dashboard_html():
    """Serve the facilitator dashboard HTML page (alternative route)"""
    try:
        # Read the facilitator dashboard HTML file
        import os
        dashboard_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'facilitator_dashboard.html')
        
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Set proper content type
        from flask import Response
        return Response(html_content, mimetype='text/html')
    except FileNotFoundError:
        return "Facilitator dashboard not found", 404
    except Exception as e:
        current_app.logger.error(f"Error serving facilitator dashboard: {str(e)}")
        return "Internal server error", 500 