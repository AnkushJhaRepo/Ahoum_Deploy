#!/usr/bin/env python3
"""
Debug script for Flask server issues

This script helps identify common problems with the Flask application.
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = [
        'SECRET_KEY',
        'SQLALCHEMY_DATABASE_URI',
        'JWT_SECRET_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * len(value)} (set)")
        else:
            print(f"❌ {var}: NOT SET")
            missing_vars.append(var)
    
    return missing_vars

def check_database():
    """Check if database file exists"""
    print("\n🗄️ Checking database...")
    
    db_path = Path("instance/app.db")
    if db_path.exists():
        print(f"✅ Database file exists: {db_path}")
        print(f"   Size: {db_path.stat().st_size} bytes")
    else:
        print(f"❌ Database file not found: {db_path}")
        return False
    
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_jwt_extended',
        'flask_migrate',
        'bcrypt',
        'pyjwt'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    return missing_packages

def create_env_file():
    """Create a .env file with default values"""
    print("\n📝 Creating .env file...")
    
    env_content = """# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
SQLALCHEMY_DATABASE_URI=sqlite:///instance/app.db
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

# Optional: Google OAuth (if using)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# CRM Microservice Configuration
CRM_BASE_URL=http://localhost:5001
CRM_AUTH_TOKEN=your-secret-token
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with default values")
    print("⚠️  Remember to change the secret keys in production!")

def run_server():
    """Run the Flask server with debug mode"""
    print("\n🚀 Starting Flask server...")
    
    # Set environment variables if not already set
    if not os.getenv('SECRET_KEY'):
        os.environ['SECRET_KEY'] = 'debug-secret-key'
    if not os.getenv('SQLALCHEMY_DATABASE_URI'):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
    if not os.getenv('JWT_SECRET_KEY'):
        os.environ['JWT_SECRET_KEY'] = 'debug-jwt-secret-key'
    
    # Set debug mode
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    try:
        from main_app.app import create_app
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\n🔧 Try running these commands:")
        print("   python -m flask db upgrade")
        print("   python main.py")

def main():
    """Main debug function"""
    print("🐛 Flask Server Debug Tool")
    print("=" * 40)
    
    # Check dependencies
    missing_packages = check_dependencies()
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("💡 Install them with: pip install -r main_app/requirements.txt")
        return
    
    # Check environment
    missing_vars = check_environment()
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        create_env_file()
        print("\n💡 After creating .env file, restart the server")
        return
    
    # Check database
    if not check_database():
        print("\n💡 Database will be created automatically when you start the server")
    
    print("\n✅ All checks passed!")
    print("\n🚀 Starting server...")
    run_server()

if __name__ == "__main__":
    main() 