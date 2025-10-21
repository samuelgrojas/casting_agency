import os
from pathlib import Path

basedir = Path(__file__).resolve().parent

class Config:
    # usa DATABASE_URL si existe (útil para despliegue), si no caerá a sqlite local
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f"sqlite:///{basedir / 'database/casting_agency.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')

    # Auth0 (se usan desde auth/auth.py)
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', '')
    AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE', '')
    AUTH0_ALGORITHMS = os.getenv('AUTH0_ALGORITHMS', 'RS256')