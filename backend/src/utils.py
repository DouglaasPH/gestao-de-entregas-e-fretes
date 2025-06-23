from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from src.models import User, db
from functools import wraps


def requires_role(roles_name_array):
    """
    Decorator to restrict access to endpoints based on user roles.

    Args:
        roles_name_array (list): A list of allowed role names.

    Returns:
        function: The decorated function, executed only if the user has one of the allowed roles.

    Behavior:
        - Retrieves the current user ID from the JWT token.
        - Checks if the user's role is present in roles_name_array.
        - If the user does not have permission, returns HTTP 403 Forbidden with an error message.
        - If authorized, executes the original function.
    """
    def decorator(f):
        @wraps(f)  # Preserves metadata of the original function
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()  # Get the user ID from the JWT token
            user = db.get_or_404(User, user_id)  # Retrieve the user from DB, or return 404 if not found

            if user.role.name not in roles_name_array:
                return {'message': 'User does not have access.'}, HTTPStatus.FORBIDDEN

            return f(*args, **kwargs)  # Proceed if the user has the required role
        return wrapped
    return decorator
