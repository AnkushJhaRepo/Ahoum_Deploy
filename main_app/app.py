from flask import Flask
from flask_cors import CORS
from main_app.config import Config
from main_app.models import db, migrate
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS with specific configuration to prevent cross-tab conflicts
    CORS(app, 
         origins=['http://127.0.0.1:5500', 'http://localhost:5500', 'http://localhost:3000'],
         supports_credentials=True,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         expose_headers=['Content-Type', 'Authorization'],
         max_age=3600)

    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize JWT
    jwt = JWTManager(app)

    @app.route("/")
    def index():
        return "Server running"

    @app.route("/health")
    def health():
        return {"status": "healthy", "service": "main-event-app"}

    # Import and register blueprints/routes here
    from main_app.routes.auth_routes import auth_bp
    from main_app.routes.event_routes import event_bp
    from main_app.routes.booking_routes import booking_bp
    from main_app.routes.facilitator_routes import facilitator_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(event_bp, url_prefix='/api')
    app.register_blueprint(booking_bp, url_prefix='/api/bookings')
    app.register_blueprint(facilitator_bp, url_prefix='/api/facilitator')

    return app

