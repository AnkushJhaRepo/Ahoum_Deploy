import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    
    # Get database URI from environment or use default with absolute path
    default_db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
    if not default_db_uri:
        # Use absolute path to the project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, 'instance', 'app.db')
        # Use proper SQLite URI format with 4 slashes for absolute path
        default_db_uri = f'sqlite:///{db_path}'
    
    SQLALCHEMY_DATABASE_URI = default_db_uri
    
    # SQLite configuration for web applications
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'timeout': 20,
            'check_same_thread': False
        }
    }
    
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'myjwtsecret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    
    # CRM Service Configuration
    CRM_BASE_URL = os.getenv('CRM_BASE_URL', 'http://localhost:5001')
    CRM_AUTH_TOKEN = os.getenv('CRM_AUTH_TOKEN', 'your-static-bearer-token-here')

class DevConfig(Config):
    DEBUG = True
