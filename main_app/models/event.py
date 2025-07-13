from main_app.models import db
from datetime import datetime

class Event(db.Model):
    """Event model for storing event information"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('Session', backref='parent_event', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Event {self.title}>'
    
    def to_dict(self):
        """Convert event to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'sessions_count': 0  # Will be calculated when needed
        }
    
    @property
    def is_active(self):
        """Check if event is currently active"""
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date
    
    @property
    def is_upcoming(self):
        """Check if event is upcoming"""
        now = datetime.utcnow()
        return self.start_date > now
    
    @property
    def is_past(self):
        """Check if event is in the past"""
        now = datetime.utcnow()
        return self.end_date < now
