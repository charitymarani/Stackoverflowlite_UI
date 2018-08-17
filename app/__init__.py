'''
___init__.py
main config  file
'''

from flask import Flask, request, jsonify
from config import CONFIG
from flask_jwt_extended import (JWTManager, jwt_required,
                                create_access_token, get_raw_jwt)
from app.api.v1.question.views import qn
from app.api.v1.auth.views import auth
APP = Flask(__name__, template_folder='./templates',
            static_folder='./static')

''' function that receives configaration and creates the app'''
JWT = JWTManager(APP)
@APP.errorhandler(400)
def bad_request(error):
    '''error handler for Bad request'''
    return jsonify(dict(error='Bad request')), 400


@APP.errorhandler(404)
def page_not_found(error):
    '''error handler for 404'''
    return jsonify(dict(error='Page not found')), 404


@APP.errorhandler(405)
def unauthorized(error):
    '''error handler for 405'''
    return jsonify(dict(error='Method not allowed')), 405


@APP.errorhandler(500)
def internal_server_error(error):
    '''error handler for 500'''
    return jsonify(dict(error='Internal server error')), 500
  
def create_app(config):
    APP.config.from_object(CONFIG[config])
    APP.url_map.strict_slashes = False

    APP.register_blueprint(auth)
    APP.register_blueprint(qn)
    return APP
