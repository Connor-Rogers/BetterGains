# decorators.py
import json
from functools import wraps
from urllib.request import urlopen

from flask import request, g
from jose import jwt

from decouple import config


def require_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token()
        jsonurl = urlopen(
            f'https://{config("AUTH0_DOMAIN")}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=config("ALGORITHMS"),
                    audience=config("API_AUDIENCE"),
                    issuer=f'https://{config("AUTH0_DOMAIN")}/'
                )
                g.current_user = payload
                return f(*args, **kwargs)
        except jwt.JWTError as error:
            print(f'Error: {error}')
        return {'message': 'Unauthorized'}, 401

    return decorated


def get_token():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise jwt.JWTError('Authorization header is missing')

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise jwt.JWTError('Invalid header: must start with "Bearer"')
    elif len(parts) == 1:
        raise jwt.JWTError('Invalid header: token missing')
    elif len(parts) > 2:
        raise jwt.JWTError('Invalid header: contains extra content')

    token = parts[1]
    return token
