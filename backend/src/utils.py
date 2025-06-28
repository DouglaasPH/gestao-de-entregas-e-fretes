from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import abort

from src.models import User, db
from functools import wraps
from src.models import User


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


@jwt_required()
def get_authenticated_user():
    user_id = get_jwt_identity()

    return User.query.get_or_404(user_id)


def is_self_user(user_id_to_modify_or_views):
    current_user = get_authenticated_user()

    if current_user.id != user_id_to_modify_or_views:
        return False
    else:
        return True


def get_authorized_user_or_abort(user_id_to_modify_or_views):
    current_user = get_authenticated_user()
    
    # Admin can modify any user
    if current_user.role.name == 'admin':
        return  db.get_or_404(User, user_id_to_modify_or_views)
    else:
        # Others can only modify themselves
        if not is_self_user(user_id_to_modify_or_views):
            abort(HTTPStatus.FORBIDDEN, description='You can only edit your own data.')
        else:
            return current_user