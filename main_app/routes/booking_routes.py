from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from main_app.models import db
from main_app.models.booking import Booking, BookingStatus
from main_app.models.session import Session
from main_app.models.user import User
from main_app.services.notify_crm import CRMNotificationService
from datetime import datetime
from sqlalchemy import desc

booking_bp = Blueprint('bookings', __name__)

def send_crm_notification(booking, user, session, action="created"):
    """Send CRM notification for booking actions"""
    try:
        crm_service = CRMNotificationService()
        
        # Prepare notification data
        notification_data = {
            'session_name': f"{session.parent_event.title} - {session.location}",
            'session_time': session.time.isoformat(),
            'session_location': session.location,
            'facilitator_name': session.facilitator.name if session.facilitator else "Unknown"
        }
        
        # Send notification to CRM
        crm_service.send_booking_notification(
            booking_id=booking.id,
            user_id=user.id,
            session_id=session.id,
            action=action,
            additional_data=notification_data
        )
        
        current_app.logger.info(f"CRM notification sent for booking {booking.id} - {action}")
        
    except Exception as e:
        # Log error but don't fail the booking operation
        current_app.logger.error(f"Failed to send CRM notification for booking {booking.id}: {str(e)}")

@booking_bp.route('/book', methods=['POST'])
@jwt_required()
def book_session():
    """Book a session for the authenticated user"""
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        
        # Get current user
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        session_id = data.get('session_id')
        
        # Validate required fields
        if not session_id:
            return jsonify({'error': 'session_id is required'}), 400
        
        # Check if session exists
        session = Session.query.get(session_id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Check if session is in the past
        if session.is_past:
            return jsonify({'error': 'Cannot book a session that has already passed'}), 400
        
        # Check if user already has an active booking for this session
        existing_booking = Booking.query.filter_by(
            user_id=current_user_id,
            session_id=session_id,
            status=BookingStatus.BOOKED.value
        ).first()
        
        if existing_booking:
            return jsonify({'error': 'You already have an active booking for this session'}), 409
        
        # Check if user has a cancelled booking for this session
        cancelled_booking = Booking.query.filter_by(
            user_id=current_user_id,
            session_id=session_id,
            status=BookingStatus.CANCELLED.value
        ).first()
        
        if cancelled_booking:
            # Reactivate the cancelled booking
            cancelled_booking.reactivate()
            db.session.commit()
            
            # Send CRM notification for reactivation
            send_crm_notification(cancelled_booking, current_user, session, "reactivated")
            
            return jsonify({
                'message': 'Booking reactivated successfully',
                'booking': cancelled_booking.to_dict()
            }), 200
        
        # Create new booking
        new_booking = Booking()
        new_booking.user_id = current_user_id
        new_booking.session_id = session_id
        new_booking.status = BookingStatus.BOOKED.value
        new_booking.timestamp = datetime.utcnow()
        
        # Save to database
        db.session.add(new_booking)
        db.session.commit()
        
        # Send CRM notification for new booking
        send_crm_notification(new_booking, current_user, session, "created")
        
        return jsonify({
            'message': 'Session booked successfully',
            'booking': new_booking.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in book_session: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@booking_bp.route('/my-bookings', methods=['GET'])
@jwt_required()
def get_my_bookings():
    """Get all bookings for the authenticated user"""
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', type=str)  # booked, cancelled, all
        
        # Validate status parameter
        if status and status not in ['booked', 'cancelled', 'all']:
            return jsonify({'error': 'Invalid status parameter. Use: booked, cancelled, or all'}), 400
        
        # Build query
        query = Booking.query.filter_by(user_id=current_user_id)
        
        # Apply status filter
        if status and status != 'all':
            query = query.filter_by(status=status)
        
        # Order by timestamp (newest first)
        query = query.order_by(desc(Booking.timestamp))
        
        # Apply pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        bookings = pagination.items
        
        # Convert to dictionary format
        bookings_data = []
        for booking in bookings:
            booking_dict = booking.to_dict()
            bookings_data.append(booking_dict)
        
        return jsonify({
            'bookings': bookings_data,
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

@booking_bp.route('/cancel/<int:booking_id>', methods=['POST'])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking for the authenticated user"""
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        
        # Get the booking
        booking = Booking.query.get_or_404(booking_id)
        
        # Check if the booking belongs to the current user
        if booking.user_id != current_user_id:
            return jsonify({'error': 'You can only cancel your own bookings'}), 403
        
        # Check if booking is already cancelled
        if booking.is_cancelled:
            return jsonify({'error': 'Booking is already cancelled'}), 400
        
        # Check if session has already passed
        if booking.session.is_past:
            return jsonify({'error': 'Cannot cancel booking for a session that has already passed'}), 400
        
        # Cancel the booking
        booking.cancel()
        db.session.commit()
        
        return jsonify({
            'message': 'Booking cancelled successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@booking_bp.route('/reactivate/<int:booking_id>', methods=['POST'])
@jwt_required()
def reactivate_booking(booking_id):
    """Reactivate a cancelled booking for the authenticated user"""
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        
        # Get current user
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get the booking
        booking = Booking.query.get_or_404(booking_id)
        
        # Check if the booking belongs to the current user
        if booking.user_id != current_user_id:
            return jsonify({'error': 'You can only reactivate your own bookings'}), 403
        
        # Check if booking is already active
        if booking.is_active:
            return jsonify({'error': 'Booking is already active'}), 400
        
        # Check if session has already passed
        if booking.session.is_past:
            return jsonify({'error': 'Cannot reactivate booking for a session that has already passed'}), 400
        
        # Check if user already has an active booking for this session
        existing_booking = Booking.query.filter_by(
            user_id=current_user_id,
            session_id=booking.session_id,
            status=BookingStatus.BOOKED.value
        ).first()
        
        if existing_booking:
            return jsonify({'error': 'You already have an active booking for this session'}), 409
        
        # Reactivate the booking
        booking.reactivate()
        db.session.commit()
        
        # Send CRM notification for reactivation
        send_crm_notification(booking, current_user, booking.session, "reactivated")
        
        return jsonify({
            'message': 'Booking reactivated successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in reactivate_booking: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@booking_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """Get a specific booking for the authenticated user"""
    try:
        # Get current user ID from JWT
        current_user_id = get_jwt_identity()
        
        # Get the booking
        booking = Booking.query.get_or_404(booking_id)
        
        # Check if the booking belongs to the current user
        if booking.user_id != current_user_id:
            return jsonify({'error': 'You can only view your own bookings'}), 403
        
        return jsonify(booking.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
