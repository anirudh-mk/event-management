from functools import wraps

from utils.permissions import JWTToken


def role_required():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(obj, request, *args, **kwargs):
            user_id = JWTToken.fetch_user_id(request)
            return view_func(obj, request, *args, **kwargs)
        return _wrapped_view
    return decorator
