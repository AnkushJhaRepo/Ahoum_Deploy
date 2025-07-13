import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app
from typing import Optional, Dict, Any

class AuthService:
    """Service class for authentication-related operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password as string
        """
        try:
            # Convert password to bytes
            password_bytes = password.encode('utf-8')
            
            # Generate salt and hash password
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)
            
            # Return hashed password as string
            return hashed.decode('utf-8')
        except Exception as e:
            raise Exception(f"Error hashing password: {str(e)}")
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash using bcrypt
        
        Args:
            password (str): Plain text password to verify
            hashed_password (str): Hashed password from database
            
        Returns:
            bool: True if password matches, False otherwise
        """
        try:
            # Convert both to bytes
            password_bytes = password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            
            # Verify password
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception as e:
            # Log error but don't expose details
            current_app.logger.error(f"Error verifying password: {str(e)}")
            return False
    
    @staticmethod
    def generate_jwt(user_id: int, additional_claims: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a JWT token for a user
        
        Args:
            user_id (int): User ID to include in token
            additional_claims (dict, optional): Additional claims to include in token
            
        Returns:
            str: JWT token string
        """
        try:
            # Get JWT secret key from config
            secret_key = current_app.config.get('JWT_SECRET_KEY')
            if not secret_key:
                raise Exception("JWT_SECRET_KEY not configured")
            
            # Prepare payload
            payload = {
                'sub': str(user_id),  # Flask-JWT-Extended expects 'sub' claim as string
                'user_id': user_id,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(hours=24)  # 24 hour expiration
            }
            
            # Add additional claims if provided
            if additional_claims:
                payload.update(additional_claims)
            
            # Generate JWT token
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            return token
            
        except Exception as e:
            raise Exception(f"Error generating JWT: {str(e)}")
    
    @staticmethod
    def verify_jwt(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token
        
        Args:
            token (str): JWT token to verify
            
        Returns:
            dict: Decoded token payload if valid, None otherwise
        """
        try:
            # Get JWT secret key from config
            secret_key = current_app.config.get('JWT_SECRET_KEY')
            if not secret_key:
                raise Exception("JWT_SECRET_KEY not configured")
            
            # Decode and verify token
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
            
        except jwt.ExpiredSignatureError:
            current_app.logger.warning("JWT token has expired")
            return None
        except jwt.InvalidTokenError as e:
            current_app.logger.warning(f"Invalid JWT token: {str(e)}")
            return None
        except Exception as e:
            current_app.logger.error(f"Error verifying JWT: {str(e)}")
            return None
    
    @staticmethod
    def get_user_id_from_token(token: str) -> Optional[int]:
        """
        Extract user ID from JWT token
        
        Args:
            token (str): JWT token
            
        Returns:
            int: User ID if token is valid, None otherwise
        """
        payload = AuthService.verify_jwt(token)
        if payload:
            return payload.get('user_id')
        return None
    
    @staticmethod
    def refresh_jwt(token: str) -> Optional[str]:
        """
        Refresh a JWT token (extend expiration)
        
        Args:
            token (str): Current JWT token
            
        Returns:
            str: New JWT token if original is valid, None otherwise
        """
        payload = AuthService.verify_jwt(token)
        if payload:
            user_id = payload.get('user_id')
            if user_id:
                # Remove timestamp fields from payload
                additional_claims = {k: v for k, v in payload.items() 
                                   if k not in ['user_id', 'iat', 'exp']}
                return AuthService.generate_jwt(user_id, additional_claims)
        return None
