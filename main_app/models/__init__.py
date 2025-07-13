from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from main_app.models.user import User
from main_app.models.event import Event
from main_app.models.session import Session
from main_app.models.booking import Booking, BookingStatus
