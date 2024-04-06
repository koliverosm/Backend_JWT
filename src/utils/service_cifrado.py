from decouple import config
from flask import jsonify
import datetime
import jwt
import pytz


class Security():

    secret = config('JWT_KEY')
    tz = pytz.timezone("America/Bogota")

    @classmethod
    def generate_token(cls, authenticated_user):
        payload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=2),
            'username': authenticated_user.get_username(),
            'roles': authenticated_user.get_roles()

        }

        return jwt.encode(payload, cls.secret, algorithm="HS256")

    @classmethod
    def verify_token(cls, headers):
        authenticated = False
        decoded_token = None

        if 'Authorization' in headers:

            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if len(encoded_token) > 0:
                try:
                    payload = jwt.decode(
                        encoded_token, cls.secret, algorithms=["HS256"])
                    roles = payload['roles']

                    if 'admin' in roles:
                        authenticated = True
                    elif 'user' in roles:
                        authenticated = True

                    decoded_token = payload

                except jwt.ExpiredSignatureError:
                    # Excepción cuando la firma del token ha expirado
                    print("token expired")
                    return False, "token expired"

                except jwt.InvalidSignatureError:
                    # Excepción cuando la firma del token es inválida
                    print("token is invalid")
                    return False, 'token invalid'

                except jwt.DecodeError:
                    # Excepción cuando hay un error de decodificación
                    print("error de decodificación")
                    return False, None

            else:
                # No se proporcionó un token válido
                authenticated = False
        return authenticated, decoded_token
