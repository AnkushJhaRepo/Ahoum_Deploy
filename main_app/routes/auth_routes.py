from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main_app.models import db
from main_app.models.user import User
from main_app.routes.auth_service import AuthService
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    return True, ""

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract user data
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        # Validate required fields
        if not all([name, email, password]):
            return jsonify({'error': 'Name, email, and password are required'}), 400
        
        # Validate email format
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        is_valid_password, password_error = validate_password(password)
        if not is_valid_password:
            return jsonify({'error': password_error}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Create new user with hashed password
        hashed_password = AuthService.hash_password(password)
        new_user = User()
        new_user.name = name
        new_user.email = email
        new_user.password = hashed_password
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
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
        db.session.rollback()
        import traceback
        print(f"❌ Registration error: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract login data
        email = data.get('email')
        password = data.get('password')
        
        # Validate required fields
        if not all([email, password]):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if not user or not AuthService.verify_password(password, user.password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate JWT token
        access_token = AuthService.generate_jwt(user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
