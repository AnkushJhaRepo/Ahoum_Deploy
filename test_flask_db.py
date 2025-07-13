import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Add the main_app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'main_app'))

from main_app.config import DevConfig

def test_flask_db_connection():
    """Test if Flask-SQLAlchemy can connect to the database"""
    print("🔍 Testing Flask-SQLAlchemy database connection...")
    
    # Create a minimal Flask app
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    
    print(f"📁 Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Initialize SQLAlchemy
    db = SQLAlchemy(app)
    
    try:
        with app.app_context():
            # Test the connection
            print("🔓 Attempting to connect to database...")
            db.engine.connect()
            print("✅ Successfully connected to database!")
            
            # Test a simple query
            print("🔍 Testing a simple query...")
            with db.engine.connect() as conn:
                result = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='table';"))
                tables = [row[0] for row in result]
                print(f"📋 Found tables: {tables}")
            
            # Test User model - we need to import it after db is initialized
            print("👤 Testing User model...")
            
            # Define a simple User model for testing
            class User(db.Model):
                __tablename__ = 'users'
                id = db.Column(db.Integer, primary_key=True)
                name = db.Column(db.String(50), nullable=False)
                email = db.Column(db.String(100), unique=True, nullable=False)
                password = db.Column(db.String(100), nullable=False)
            
            # Test query
            user_count = User.query.count()
            print(f"📊 Total users in database: {user_count}")
            
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_flask_db_connection() 