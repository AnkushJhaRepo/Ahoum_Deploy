from main_app.models import db
from datetime import datetime, timedelta

class Session(db.Model):
    """Session model for storing session information within events"""
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    facilitator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    facilitator = db.relationship('User', backref='facilitated_sessions', lazy=True)
    bookings = db.relationship('Booking', backref='session', lazy=True, cascade='all, delete-orphan')
    # Note: event relationship is defined in Event model with backref='parent_event'
    
    def __repr__(self):
        return f'<Session {self.id} for Event {self.event_id}>'
    
    def to_dict(self):
        """Convert session to dictionary"""
        return {
            'id': self.id,
            'event_id': self.event_id,
            'facilitator_id': self.facilitator_id,
            'time': self.time.isoformat() if self.time else None,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'facilitator_name': self.facilitator.name if self.facilitator else None,
            'event_title': self.parent_event.title if self.parent_event else None
        }
    
    @property
    def is_upcoming(self):
        """Check if session is upcoming"""
        now = datetime.utcnow()
        return self.time > now
    
    @property
    def is_past(self):
        """Check if session is in the past"""
        now = datetime.utcnow()
        return self.time < now
    
    @property
    def is_ongoing(self):
        """Check if session is currently ongoing (within 2 hours of start time)"""
        now = datetime.utcnow()
        session_end = self.time + timedelta(hours=2)  # Assuming 2-hour sessions
        return self.time <= now <= session_end
