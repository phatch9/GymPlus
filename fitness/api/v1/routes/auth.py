"""
Auth API Routes
RESTful endpoints for authentication
"""

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from fitness import db, bcrypt
from fitness.models import User
from fitness.api.v1.schemas import UserSchema
from fitness.api.v1.services.user_service import UserService
from fitness.api.v1.middleware import AppError, ValidationFailedError
from marshmallow import ValidationError

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
user_service = UserService()


@bp.route('/signup', methods=['POST'])
def signup():
    """Register a new user"""
    try:
        schema = UserSchema()
        data = schema.load(request.get_json() or {})
        
        # Create user
        user_data = user_service.create_user(data)
        
        # Get the created user and login
        user = User.query.get(user_data['id'])
        login_user(user)
        
        return jsonify({
            'message': 'User created successfully',
            'user': user_data
        }), 201
    
    except ValidationError as e:
        raise ValidationFailedError("Validation failed", e.messages)
    except ValueError as e:
        raise AppError(str(e), 400)
    except Exception as e:
        raise AppError(f"Error creating user: {str(e)}", 500)


@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            raise ValidationFailedError(
                "Validation failed",
                {'email': ['Email is required'], 'password': ['Password is required']}
            )
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            raise AppError("Invalid email or password", 401)
        
        # Login user
        login_user(user)
        
        # Return user data
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'calories_consumed': user.calories_consumed,
            'calories_burned': user.calories_burned,
            'user_perk': user.user_perk,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }
        
        return jsonify({
            'message': 'Login successful',
            'user': user_data
        }), 200
    
    except Exception as e:
        raise AppError(f"Error during login: {str(e)}", 500)


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout user"""
    try:
        logout_user()
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        raise AppError(f"Error during logout: {str(e)}", 500)


@bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current logged-in user"""
    try:
        user_data = {
            'id': current_user.id,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'email': current_user.email,
            'calories_consumed': current_user.calories_consumed,
            'calories_burned': current_user.calories_burned,
            'user_perk': current_user.user_perk,
            'created_at': current_user.created_at.isoformat(),
            'updated_at': current_user.updated_at.isoformat()
        }
        return jsonify(user_data), 200
    except Exception as e:
        raise AppError(f"Error retrieving user: {str(e)}", 500)
