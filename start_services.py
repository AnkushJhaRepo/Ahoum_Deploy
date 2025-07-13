#!/usr/bin/env python3
"""
Script to start both the main Flask app and CRM microservice
with proper configuration to prevent reloads
"""

import subprocess
import sys
import os
import time
import signal
import threading

def start_main_app():
    """Start the main Flask application"""
    print("🚀 Starting main Flask application...")
    
    # Set environment variables
    env = os.environ.copy()
    env['FLASK_APP'] = 'main_app.app'
    env['FLASK_ENV'] = 'production'  # Disable debug mode
    env['FLASK_DEBUG'] = 'false'  # Explicitly disable debug mode
    
    # Start the main app
    process = subprocess.Popen([
        sys.executable, 'main.py'
    ], env=env)
    
    print(f"✅ Main app started with PID: {process.pid}")
    return process

def start_crm_service():
    """Start the CRM microservice"""
    print("🚀 Starting CRM microservice...")
    
    # Set environment variables
    env = os.environ.copy()
    env['CRM_DEBUG'] = 'false'  # Disable debug mode
    env['CRM_PORT'] = '5001'
    env['FLASK_DEBUG'] = 'false'  # Explicitly disable Flask debug mode
    
    # Start the CRM service
    process = subprocess.Popen([
        sys.executable, 'crm_microservice/crm_app.py'
    ], env=env)
    
    print(f"✅ CRM service started with PID: {process.pid}")
    return process

def main():
    """Main function to start both services"""
    print("🎯 Starting Event Management System...")
    print("=" * 50)
    
    # Start both services
    main_process = start_main_app()
    crm_process = start_crm_service()
    
    print("\n" + "=" * 50)
    print("✅ Both services are starting...")
    print("📱 Main app will be available at: http://localhost:5000")
    print("📊 CRM service will be available at: http://localhost:5001")
    print("📋 CRM notifications dashboard: http://localhost:5001/dashboard")
    print("\nPress Ctrl+C to stop both services")
    print("=" * 50)
    
    try:
        # Wait for both processes
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if main_process.poll() is not None:
                print("❌ Main app stopped unexpectedly")
                break
                
            if crm_process.poll() is not None:
                print("❌ CRM service stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        # Terminate processes gracefully
        main_process.terminate()
        crm_process.terminate()
        
        # Wait for them to stop
        try:
            main_process.wait(timeout=5)
            crm_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("⚠️ Force killing processes...")
            main_process.kill()
            crm_process.kill()
        
        print("✅ Services stopped")

if __name__ == '__main__':
    main() 