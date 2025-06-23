from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity
from src.models import User, db
from functools import wraps

# Decorator to restrict access based on user role
def requires_role(role_name):
    def decorator(f):
        @wraps(f) # Preserves the original function's name and docstring
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity() # Get the user ID from the JWT token
            user = db.get_or_404(User, user_id)  # Retrieve the user from the database by ID or return 404 if not found
            
            # Check if the user's role matches the required role
            if user.role.name != role_name:
                # If not, return a 403 Forbidden response
                return { 'message': 'User does not have access.' }, HTTPStatus.FORBIDDEN
            # If the role matches, execute the original function
            return f(*args, **kwargs)
        return wrapped  # Return the wrapped function
    return decorator  # Return the decorator itself
