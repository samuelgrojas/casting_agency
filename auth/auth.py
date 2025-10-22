import os
import json
from dotenv import load_dotenv
from flask import request
from functools import wraps, lru_cache
from jose import jwt
from urllib.request import urlopen
from urllib.error import URLError

# load .env from project root
load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = os.getenv('AUTH0_ALGORITHMS').split(',')
API_AUDIENCE = os.getenv('AUTH0_AUDIENCE')

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    if len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    if len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

def check_permissions(permission, payload):
    perms = payload.get('permissions', [])
    if not isinstance(perms, list):
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions claim malformed.'
        }, 400)

    if permission not in perms:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True

@lru_cache(maxsize=1)
def _get_jwks():
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    try:
        with urlopen(jwks_url) as res:
            return json.loads(res.read())
    except URLError:
        raise AuthError({
            'code': 'jwks_fetch_error',
            'description': 'Unable to fetch JWKS from Auth0.'
        }, 500)

def verify_decode_jwt(token):
    jwks = _get_jwks()

    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Invalid header. Could not parse authentication token.'
        }, 401)

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    rsa_key = {}
    for key in jwks.get('keys', []):
        if key.get('kid') == unverified_header.get('kid'):
            rsa_key = {
                'kty': key.get('kty'),
                'kid': key.get('kid'),
                'use': key.get('use'),
                'n': key.get('n'),
                'e': key.get('e')
            }
            break

    if not rsa_key:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 401)

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f'https://{AUTH0_DOMAIN}/'
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token expired.'
        }, 401)

    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Incorrect claims. Check audience and issuer.'
        }, 401)

    except Exception:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            # pass payload as first arg to route handlers (app.py already expects this)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator