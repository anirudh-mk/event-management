from functools import wraps

from rest_framework import status
from rest_framework.response import Response
from utils.permissions import JWTToken
from rest_framework import status


def role_required(roles):
    def decorator(view_func):
        def wrapped_view_func(obj, request, *args, **kwargs):
            user = request.user
            if not any(getattr(user, role, False) for role in roles):
                return Response(
                    data={"error": "unauthorized request"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return view_func(obj, request, *args, **kwargs)
        return wrapped_view_func
    return decorator
