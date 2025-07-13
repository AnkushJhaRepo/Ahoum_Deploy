#!/usr/bin/env python3
import webbrowser
import time

def open_facilitator_dashboard():
    """Open the facilitator dashboard in the browser"""
    print("=== Opening Facilitator Dashboard ===\n")
    
    # First, open the main application
    main_url = "http://127.0.0.1:5500/index.html"
    print(f"1. Opening main application: {main_url}")
    webbrowser.open(main_url)
    
    time.sleep(2)
    
    # Then open the facilitator dashboard
    dashboard_url = "http://localhost:5000/api/facilitator/dashboard-page"
    print(f"2. Opening facilitator dashboard: {dashboard_url}")
    webbrowser.open(dashboard_url)
    
    print("\n=== Testing Instructions ===")
    print("1. In the main application (port 5500):")
    print("   - Login with facilitator credentials:")
    print("     Email: facilitator_gvt2zb@test.com")
    print("     Password: v0oz2nqGvJ")
    print("   - Click the 'Facilitator Dashboard' button")
    
    print("\n2. In the facilitator dashboard (port 5000):")
    print("   - You should see the dashboard with tabs: Dashboard, Sessions, Users")
    print("   - Go to the 'Sessions' tab")
    print("   - You should see 1 session: 'Yoga Wellness Retreat' at 'Test Room 101'")
    print("   - Try clicking the 'Cancel' button on the session")
    print("   - Confirm the cancellation when prompted")
    
    print("\n3. Expected behavior:")
    print("   - Session should be cancelled successfully")
    print("   - You should see a success message")
    print("   - The session should disappear from the list")
    
    print("\n=== Troubleshooting ===")
    print("If you get redirected to the main page:")
    print("- Make sure you're logged in as the facilitator")
    print("- Check that the token is stored in localStorage")
    print("- Try refreshing the dashboard page")

if __name__ == "__main__":
    open_facilitator_dashboard() 