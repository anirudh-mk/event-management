from datetime import datetime, timedelta
import jwt
from rest_framework.permissions import BasePermission
from rest_framework import authentication
from rest_framework.serializers import ValidationError
from api.models import User


class CustamizePermission(BasePermission):
    def authenticate(self, request):
        try:
            token = authentication.get_authorization_header(request).decode('utf-8').split()
            if token[0] != "Bearer" and len(token) != 2:
                raise ValidationError({"error": "invalid token"})
            return self._authenticate_credentials(request, token[1])
        except Exception:
            raise ValidationError({"error": "invalid token"})

    def _authenticate_credentials(self, request, token):
        payload = jwt.decode(token, 'SEDKLK23D@LK323#@!2', algorithms=["HS256"], verify=True)

        id = payload.get("id", None)
        expiry = payload.get("expiry", None)

        if id and expiry:
            # if expiry check expiry and return Token Expired
            user = User.objects.filter(id=id)
            if user.exists():
                return user.first(), payload
            else:
                pass
        return None, payload


class JWTToken:
    def generate(self, user):
        if user is not None:
            access_expiry_time = datetime.now() + timedelta(minutes=5)
            access_expiry = access_expiry_time.strftime("%d/%m/%Y %H:%M:%S")
            access_token = jwt.encode(
                {
                    "id": user.id,
                    'expiry': access_expiry,
                    'token_type': 'access'
                },
                "SEDKLK23D@LK323#@!2",
                algorithm="HS256"
            )

            refresh_expiry_time = datetime.now() + timedelta(days=3)
            refresh_expiry = refresh_expiry_time.strftime("%d/%m/%Y %H:%M:%S")

            refresh_token = jwt.encode(
                {
                    "id": user.id,
                    'expiry': access_expiry,
                    'token_type': 'access'
                },
                "SEDKLK23D@LK323#@!2",
                algorithm="HS256"
            )

            token = {
                'accessToken': access_token,
                'accessExpiry': access_expiry,
                'refreshToken': refresh_token,
                'refreshExpiry': refresh_expiry,
            }
        else:
            token = None
        return token

