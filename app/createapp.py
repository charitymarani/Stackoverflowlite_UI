'''
___init__.py
main config  file
'''

from flask import Flask, request, jsonify
from ..instance import settings
from flask_jwt_extended import (JWTManager, jwt_required,
                                create_access_token, get_raw_jwt)

from challenge2.app.api.v1.question.views import qn
from challenge2.app.api.v1.auth.views import auth


BLACKLIST = set()


def create_app(config):
    ''' function that receives configaration and creates the app'''
    APP = Flask(__name__)
    APP.config.from_object(settings.CONFIG[config])
    APP.url_map.strict_slashes = False
    jwt = JWTManager(APP)
    APP.register_blueprint(auth)
    APP.register_blueprint(qn)
    return APP


@jwt.token_in_blacklist_loader
def check_if_token_blacklist(decrypted_token):
    '''check if jti(unique identifier) is in black list'''
    json_token_identifier = decrypted_token['jti']
    return json_token_identifier in BLACKLIST
