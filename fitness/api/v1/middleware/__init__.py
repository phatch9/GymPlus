"""
Error handlers and custom exceptions
"""

from flask import jsonify
from marshmallow import ValidationError


class AppError(Exception):
    """Base application error"""
    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppError):
    """Resource not found error"""
    def __init__(self, message: str = "Resource not found", details: dict = None):
        super().__init__(message, 404, details)


class UnauthorizedError(AppError):
    """Authentication error"""
    def __init__(self, message: str = "Unauthorized", details: dict = None):
        super().__init__(message, 401, details)


class ForbiddenError(AppError):
    """Authorization error"""
    def __init__(self, message: str = "Forbidden", details: dict = None):
        super().__init__(message, 403, details)


class ValidationFailedError(AppError):
    """Validation error"""
    def __init__(self, message: str = "Validation failed", details: dict = None):
        super().__init__(message, 422, details)


class ConflictError(AppError):
    """Conflict error (duplicate resource)"""
    def __init__(self, message: str = "Conflict", details: dict = None):
        super().__init__(message, 409, details)


def register_error_handlers(app):
    """Register error handlers with Flask app"""
    
    @app.errorhandler(AppError)
    def handle_app_error(error):
        """Handle application errors"""
        response = {
            'error': error.__class__.__name__,
            'message': error.message,
        }
        if error.details:
            response['details'] = error.details
        return jsonify(response), error.status_code
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle Marshmallow validation errors"""
        response = {
            'error': 'ValidationError',
            'message': 'Validation failed',
            'details': error.messages
        }
        return jsonify(response), 422
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle bad request errors"""
        response = {
            'error': 'BadRequest',
            'message': 'Invalid request',
        }
        return jsonify(response), 400
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle not found errors"""
        response = {
            'error': 'NotFound',
            'message': 'Resource not found',
        }
        return jsonify(response), 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle internal server errors"""
        response = {
            'error': 'InternalServerError',
            'message': 'An unexpected error occurred',
        }
        return jsonify(response), 500
