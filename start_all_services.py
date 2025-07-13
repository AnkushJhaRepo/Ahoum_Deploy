#!/usr/bin/env python3
"""
Start both the main Flask application and CRM microservice
This file starts both services while keeping the original main.py intact
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def start_crm_service():
    """Start the CRM microservice"""
    print("Starting CRM microservice...")
    
    crm_dir = Path("crm_microservice")
    if not crm_dir.exists():
        print("CRM microservice directory not found")
        return None
    
    try:
        # Start CRM service
        crm_process = subprocess.Popen(
            [sys.executable, "crm_app.py"],
            cwd=crm_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for the service to start
        time.sleep(3)
        
        # Check if process is still running
        if crm_process.poll() is None:
            print("CRM microservice started successfully")
            return crm_process
        else:
            stdout, stderr = crm_process.communicate()
            print(f"CRM service failed to start:")
            print(f"   stdout: {stdout}")
            print(f"   stderr: {stderr}")
            return None
            
    except Exception as e:
        print(f"Error starting CRM service: {e}")
        return None

def start_main_app():
    """Start the main Flask application"""
    print("Starting main Flask application...")
    
    try:
        # Start main app using the original main.py
        main_process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for the service to start
        time.sleep(5)
        
        # Check if process is still running
        if main_process.poll() is None:
            print("Main Flask application started successfully")
            return main_process
        else:
            stdout, stderr = main_process.communicate()
            print(f"Main app failed to start:")
            print(f"   stdout: {stdout}")
            print(f"   stderr: {stderr}")
            return None
            
    except Exception as e:
        print(f"Error starting main app: {e}")
        return None

def main():
    """Main function to start both services"""
    print("Starting Event Management System with CRM Notifications")
    print("=" * 60)
    
    # Start CRM service first
    crm_process = start_crm_service()
    if not crm_process:
        print("Failed to start CRM service. Exiting.")
        return False
    
    # Start main app
    main_process = start_main_app()
    if not main_process:
        print("Failed to start main app. Stopping CRM service.")
        crm_process.terminate()
        return False
    
    print("\nBoth services started successfully!")
    print("Service URLs:")
    print("   Main App: http://localhost:5000")
    print("   CRM Service: http://localhost:5001")
    print("\nTo test the system:")
    print("   1. Open http://localhost:5000 in your browser")
    print("   2. Register/login and book a session")
    print("   3. Check CRM notifications at http://localhost:5001/notifications")
    print("\nPress Ctrl+C to stop both services")
    
    try:
        # Keep both processes running
        while True:
            time.sleep(1)
            
            # Check if either process has died
            if crm_process.poll() is not None:
                print("CRM service stopped unexpectedly")
                break
                
            if main_process.poll() is not None:
                print("Main app stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\nStopping services...")
    
    finally:
        # Clean up processes
        if crm_process and crm_process.poll() is None:
            print("Stopping CRM service...")
            crm_process.terminate()
            crm_process.wait()
            
        if main_process and main_process.poll() is None:
            print("Stopping main app...")
            main_process.terminate()
            main_process.wait()
            
        print("All services stopped")

if __name__ == "__main__":
    main() 