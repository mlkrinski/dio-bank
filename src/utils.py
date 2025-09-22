from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from src.models import User, db


def requires_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = str(get_jwt_identity())
            user = db.get_or_404(User, user_id)

            if user.role.name != role_name:
                return {"message": "User dont have acess."}, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)

        return wrapped

    return decorator


def eleva_quadrado(x):
    return x**2
