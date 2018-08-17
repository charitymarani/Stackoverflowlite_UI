'''
___init__.py
main config  file
'''

from flask import Flask, request, jsonify
from instance.config import CONFIG
from flask_jwt_extended import (JWTManager, jwt_required,
                                create_access_token, get_raw_jwt)
from app.api.v1.question.views import qn
from app.api.v1.auth.views import auth
APP = Flask(__name__, template_folder='./templates',
            static_folder='./static')

''' function that receives configaration and creates the app'''


def create_app(config):
    APP.config.from_object(CONFIG[config])
    APP.url_map.strict_slashes = False

    APP.register_blueprint(auth)
    APP.register_blueprint(qn)
    return APP
