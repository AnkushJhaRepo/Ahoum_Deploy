#!/usr/bin/env python3
import os
from main_app.app import create_app

# Set environment variables with absolute path
current_dir = os.getcwd()
db_path = os.path.join(current_dir, 'instance', 'app.db')
db_uri = f'sqlite:///{db_path}'

os.environ['SQLALCHEMY_DATABASE_URI'] = db_uri
os.environ['SECRET_KEY'] = 'supersecretkey'
os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'

app = create_app()

if __name__ == "__main__":
    print("Starting Flask server with correct configuration...")
    print(f"Database URI: {os.environ.get('SQLALCHEMY_DATABASE_URI')}")
    app.run(debug=True, host='0.0.0.0', port=5000)
