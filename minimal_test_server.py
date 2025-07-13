#!/usr/bin/env python3
"""
Minimal test server with detailed error logging
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Set environment variables
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Ahoum_Assignment\\instance\\app.db'
os.environ['SECRET_KEY'] = 'supersecretkey'
os.environ['JWT_SECRET_KEY'] = 'myjwtsecret'

# Create minimal app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

db = SQLAlchemy(app)

# Simple User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return "Minimal test server running"

@app.route('/test-register', methods=['POST'])
def test_register():
    """Test registration endpoint"""
    try:
        print("🔍 Registration request received")
        
        data = request.get_json()
        print(f"📥 Received data: {data}")
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        print(f"📋 Extracted: name={name}, email={email}, password={'*' * len(password) if password else 'None'}")
        
        if not all([name, email, password]):
            return jsonify({'error': 'Name, email, and password are required'}), 400
        
        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"⚠️ User {email} already exists")
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Create user (simple password hashing for test)
        new_user = User()
        new_user.name = name
        new_user.email = email
        new_user.password = f"hashed_{password}"  # Simple hash for testing
        
        print(f"✅ User object created: {new_user.name}")
        
        db.session.add(new_user)
        db.session.commit()
        
        print(f"✅ User saved to database with ID: {new_user.id}")
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email,
                'created_at': new_user.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        print(f"❌ Error in registration: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == "__main__":
    print("🚀 Starting minimal test server...")
    print(f"📁 Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 