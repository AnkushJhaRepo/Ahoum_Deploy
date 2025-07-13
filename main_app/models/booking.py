from main_app.models import db
from datetime import datetime
from enum import Enum

class BookingStatus(Enum):
    """Enum for booking status"""
    BOOKED = "booked"
    CANCELLED = "cancelled"

class Booking(db.Model):
    """Booking model for storing user session bookings"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=BookingStatus.BOOKED.value)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='bookings', lazy=True)
    session = db.relationship('Session', backref='bookings', lazy=True)
    
    def __repr__(self):
        return f'<Booking {self.id} - User {self.user_id} Session {self.session_id}>'
    
    def to_dict(self):
        """Convert booking to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'status': self.status,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_name': self.user.name if self.user else None,
            'user_email': self.user.email if self.user else None,
            'session_time': self.session.time.isoformat() if self.session else None,
            'session_location': self.session.location if self.session else None,
            'event_title': self.session.event.title if self.session and self.session.event else None
        }
    
    @property
    def is_active(self):
        """Check if booking is active (not cancelled)"""
        return self.status == BookingStatus.BOOKED.value
    
    @property
    def is_cancelled(self):
        """Check if booking is cancelled"""
        return self.status == BookingStatus.CANCELLED.value
    
    def cancel(self):
        """Cancel the booking"""
        self.status = BookingStatus.CANCELLED.value
        self.updated_at = datetime.utcnow()
        return self
    
    def reactivate(self):
        """Reactivate a cancelled booking"""
        self.status = BookingStatus.BOOKED.value
        self.updated_at = datetime.utcnow()
        return self
    
    @classmethod
    def get_user_bookings(cls, user_id, status=None):
        """Get all bookings for a user with optional status filter"""
        query = cls.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(cls.timestamp.desc()).all()
    
    @classmethod
    def get_session_bookings(cls, session_id, status=None):
        """Get all bookings for a session with optional status filter"""
        query = cls.query.filter_by(session_id=session_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(cls.timestamp.desc()).all()
    
    @classmethod
    def get_active_bookings(cls, session_id):
        """Get all active (booked) bookings for a session"""
        return cls.get_session_bookings(session_id, BookingStatus.BOOKED.value)
    
    @classmethod
    def count_session_bookings(cls, session_id, status=None):
        """Count bookings for a session with optional status filter"""
        query = cls.query.filter_by(session_id=session_id)
        if status:
            query = query.filter_by(status=status)
        return query.count()
    
    @classmethod
    def user_has_booking_for_session(cls, user_id, session_id):
        """Check if user has an active booking for a session"""
        return cls.query.filter_by(
            user_id=user_id,
            session_id=session_id,
            status=BookingStatus.BOOKED.value
        ).first() is not None
