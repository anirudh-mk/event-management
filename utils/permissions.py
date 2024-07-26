from datetime import datetime, timedelta
import jwt


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
