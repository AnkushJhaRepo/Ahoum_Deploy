import sqlite3
import os
from pathlib import Path

def test_database_access():
    """Test if we can access the database file"""
    db_path = r"C:\Ahoum_Assignment\instance\app.db"
    
    print(f"🔍 Testing database access...")
    print(f"📁 Database path: {db_path}")
    
    # Check if file exists
    if os.path.exists(db_path):
        print(f"✅ Database file exists")
        
        # Check file permissions
        try:
            # Try to get file info
            stat_info = os.stat(db_path)
            print(f"📊 File size: {stat_info.st_size} bytes")
            print(f"🔐 File permissions: {oct(stat_info.st_mode)}")
        except Exception as e:
            print(f"❌ Error getting file info: {e}")
        
        # Try to open with sqlite3 directly
        try:
            print(f"🔓 Attempting to open database with sqlite3...")
            conn = sqlite3.connect(db_path)
            print(f"✅ Successfully opened database connection")
            
            # Try a simple query
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📋 Found tables: {tables}")
            
            conn.close()
            print(f"✅ Successfully closed database connection")
            
        except sqlite3.OperationalError as e:
            print(f"❌ SQLite operational error: {e}")
        except Exception as e:
            print(f"❌ Error opening database: {e}")
    else:
        print(f"❌ Database file does not exist")
    
    # Check directory permissions
    instance_dir = r"C:\Ahoum_Assignment\instance"
    print(f"\n📁 Checking directory permissions...")
    print(f"📂 Instance directory: {instance_dir}")
    
    if os.path.exists(instance_dir):
        print(f"✅ Instance directory exists")
        try:
            # Try to create a test file
            test_file = os.path.join(instance_dir, "test_write.txt")
            with open(test_file, 'w') as f:
                f.write("test")
            print(f"✅ Can write to instance directory")
            os.remove(test_file)
            print(f"✅ Can delete files from instance directory")
        except Exception as e:
            print(f"❌ Cannot write to instance directory: {e}")
    else:
        print(f"❌ Instance directory does not exist")

if __name__ == "__main__":
    test_database_access() 