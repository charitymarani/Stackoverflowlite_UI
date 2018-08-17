import re
from flask import Flask, request, jsonify, render_template, Blueprint
from flask_jwt_extended import (JWTManager, jwt_required,
                                create_access_token, get_raw_jwt)
from app.api.v1.auth import auth_model
from app.api.v1.main import responses
from app.api.v1.auth.auth_model import USERS
from app import jwt



auth = Blueprint('auth', __name__)

MY_USER = auth_model.Users()


BLACKLIST = set()

'''user actions'''

@jwt.token_in_blacklist_loader
def check_if_token_blacklist(decrypted_token):
    '''check if jti(unique identifier) is in black list'''
    json_token_identifier = decrypted_token['jti']
    return json_token_identifier in BLACKLIST
@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    '''endpoint to register a user'''
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"})
    username = (data.get('username')).strip()
    name = (data.get('name')).strip()
    email = (data.get('email')).strip()
    password = (data.get('password')).strip()
    confirm_password = (data.get('confirm_password')).strip()

    if username is None or not username:
        return jsonify({"message": "Enter username"})
    if name is None or not name:
        return jsonify({"message": "Enter name"}), 206

    if len(password) < 4:
        return jsonify({"message": "password is too short"})
    if confirm_password != password:
        return jsonify({"message": "Passwords don't match"})
    b = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
    match = re.match(b, email)
    if match is None:
        return jsonify({"message": "Enter a valid email address"})
    response = jsonify(MY_USER.put(name, username, email, password))
    response.status_code = 201
    return response


@auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    '''login user by verifying password and creating an access token'''
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"})
    username = data.get('username')
    password = data.get('password')
    auth = MY_USER.verify_password(username, password)

    if auth == "True":
        access_token = create_access_token(identity=username)
        return jsonify(dict(token=access_token,
                            message="Login successful")), 200

    response = jsonify(auth)
    response.status_code = 401
    return response


@auth.route('/api/v1/auth/logout', methods=['POST'])
@jwt_required
def logout():
    '''logout user by revoking password'''
    json_token_identifier = get_raw_jwt()['jti']
    BLACKLIST.add(json_token_identifier)
    return jsonify({"message": "Successfully logged out"}), 200


@auth.route('/api/v1/auth/reset-password', methods=['POST'])
def reset_password():
    '''reset user password'''
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"})
    username = data.get("username")

    response = jsonify(MY_USER.reset_password(username))
    response.status_code = 200
    return response
