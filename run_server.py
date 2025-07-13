#!/usr/bin/env python3
"""
Run Flask server in foreground to see error messages
"""

import os
import sys

# Set environment variables
os.environ['SECRET_KEY'] = 'supersecretkey'
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'

# Import and run the app
from main_app.app import create_app

app = create_app()

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🔍 Debug mode is ON - you'll see detailed error messages")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        import traceback
        traceback.print_exc() 