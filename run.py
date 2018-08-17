"""run.py application entry point"""
import os
import app
from app import create_app

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt)
BLACKLIST = set()

config = os.environ['CONFIG_ENVIRONMENT']
APP = create_app(config)
jwt = JWTManager(APP)


@jwt.token_in_blacklist_loader
def check_if_token_blacklist(decrypted_token):
    '''check if jti(unique identifier) is in black list'''
    json_token_identifier = decrypted_token['jti']
    return json_token_identifier in BLACKLIST


if __name__ == ('__main__'):

    APP.run(Debug=True)
