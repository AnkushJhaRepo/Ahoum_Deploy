#!/usr/bin/env python3
"""
Start Flask server with correct database URI
"""

import os
import sys

# Set the correct environment variables
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Ahoum_Assignment\\instance\\app.db'
os.environ['SECRET_KEY'] = 'supersecretkey'
os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'

print("🔧 Starting Flask server with correct configuration...")
print(f"📁 Database URI: {os.environ['SQLALCHEMY_DATABASE_URI']}")
print("📍 Server will be available at: http://localhost:5000")
print("⏹️  Press Ctrl+C to stop the server")
print("-" * 50)

# Import and run the app
from main_app.app import create_app

app = create_app()

if __name__ == "__main__":
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        import traceback
        traceback.print_exc() 