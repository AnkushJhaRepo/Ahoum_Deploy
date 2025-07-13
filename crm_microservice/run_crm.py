#!/usr/bin/env python3
"""
Direct CRM service runner with visible output
Run this to start the CRM service and see all output
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Starting CRM Notification Service...")
print("=" * 50)

try:
    # Import and run the CRM app
    from crm_app import app
    
    print("CRM app imported successfully")
    print("Starting Flask server on port 5001...")
    
    # Run the app
    app.run(host='0.0.0.0', port=5001, debug=True)
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install flask flask-cors python-dotenv")
    
except Exception as e:
    print(f"Error starting CRM service: {e}")
    print("Check the error message above for details") 