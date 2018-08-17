"""run.py application entry point"""
import os
import app
from app import create_app

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt)

try:
    config = os.environ['CONFIG_ENVIRONMENT']
    APP = create_app(config)


except KeyError:
    APP = create_app('development')

if __name__ == ('__main__'):

    APP.run(Debug=True)
