from datetime import datetime, timedelta
import jwt
from rest_framework.permissions import BasePermission
from rest_framework import authentication
from rest_framework.serializers import ValidationError
from api.models import User


class CustamizePermission(BasePermission):
    """
        class for Validate access token
    """
    def authenticate(self, request):
        # check token exist in request
        try:
            # access token
            token = authentication.get_authorization_header(request).decode('utf-8').split()

            # check token is bearer
            if token[0] != "Bearer" and len(token) != 2:
                # if token is not valid rise invalid token
                raise ValidationError({"error": "invalid token"})

            # if token is valid pass to authedication credential to decode
            return self._authenticate_credentials(request, token[1])

        # catch exceptions
        except Exception:
            raise ValidationError({"error": "invalid token"})

    # authendication credentials for decode token
    def _authenticate_credentials(self, request, token):
        # decode token
        payload = jwt.decode(token, 'SEDKLK23D@LK323#@!2', algorithms=["HS256"], verify=True)

        # fetch user id and expiry from token
        id = payload.get("id", None)
        expiry = payload.get("expiry", None)

        # check id and expiry present
        if id and expiry:

            current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # check current time and expiry and return validation error
            if current_time > expiry:
                raise ValidationError({"error": "token expired"})

            # if id present fetch user
            user = User.objects.filter(id=id)
            if user.exists():

                # return user and paylod
                return user.first(), payload
            else:
                pass
        return None, payload


class JWTToken:
    """
        class for jwt authendication
    """
    # generate jwt token
    def generate(self, user):

        # check user is present
        if user is not None:
            # set access token expiry time
            access_expiry_time = datetime.now() + timedelta(minutes=5)
            access_expiry = access_expiry_time.strftime("%d/%m/%Y %H:%M:%S")

            # generate access token
            access_token = jwt.encode(
                {
                    "id": user.id,
                    'expiry': access_expiry,
                    'token_type': 'access'
                },
                "SEDKLK23D@LK323#@!2",
                algorithm="HS256"
            )

            # refresh token expiry time
            refresh_expiry_time = datetime.now() + timedelta(days=3)
            refresh_expiry = refresh_expiry_time.strftime("%d/%m/%Y %H:%M:%S")

            # generate refresh token
            refresh_token = jwt.encode(
                {
                    "id": user.id,
                    'expiry': access_expiry,
                    'token_type': 'access'
                },
                "SEDKLK23D@LK323#@!2",
                algorithm="HS256"
            )

            # create response
            token = {
                'accessToken': access_token,
                'accessExpiry': access_expiry,
                'refreshToken': refresh_token,
                'refreshExpiry': refresh_expiry,
            }
        else:
            token = None
        # return response
        return token

