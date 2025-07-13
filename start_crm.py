#!/usr/bin/env python3
"""
Start only the CRM microservice
Run this after starting the main app with: python main.py
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
        # Start CRM service with visible output
        print("Starting CRM service in crm_microservice directory...")
        crm_process = subprocess.Popen(
            [sys.executable, "crm_app.py"],
            cwd=crm_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Wait a moment for the service to start
        print("Waiting for CRM service to start...")
        time.sleep(5)
        
        # Check if process is still running
        if crm_process.poll() is None:
            print("CRM microservice started successfully!")
            print("CRM Service URL: http://localhost:5001")
            print("Dashboard URL: http://localhost:5001/dashboard")
            print("API URL: http://localhost:5001/notifications")
            print("\nPress Ctrl+C to stop the CRM service")
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

def main():
    """Main function to start CRM service"""
    print("Starting CRM Notification Service")
    print("=" * 40)
    
    # Start CRM service
    crm_process = start_crm_service()
    if not crm_process:
        print("Failed to start CRM service. Exiting.")
        print("\nTroubleshooting tips:")
        print("1. Make sure no other service is using port 5001")
        print("2. Check if you have all required dependencies installed")
        print("3. Try running manually: cd crm_microservice && python crm_app.py")
        return False
    
    try:
        # Keep the process running
        while True:
            time.sleep(1)
            
            # Check if process has died
            if crm_process.poll() is not None:
                print("CRM service stopped unexpectedly")
                stdout, stderr = crm_process.communicate()
                print(f"stdout: {stdout}")
                print(f"stderr: {stderr}")
                break
                
    except KeyboardInterrupt:
        print("\nStopping CRM service...")
    
    finally:
        # Clean up process
        if crm_process and crm_process.poll() is None:
            print("Stopping CRM service...")
            crm_process.terminate()
            crm_process.wait()
            
        print("CRM service stopped")

if __name__ == "__main__":
    main() 