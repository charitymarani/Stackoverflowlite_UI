'''auth_model.py containing models for the API authentication'''
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash


USERS = {}


class Users():
    '''class to represent users model'''

    def __init__(self):
        self.user = {}

    def put(self, name, username, email, password):
        '''add a user to USERS'''
        if username in USERS:
            return {"message": "Username already exists"}
        self.user["name"] = name
        self.user["email"] = email
        pw_hash = generate_password_hash(password)
        self.user["password"] = pw_hash

        USERS[username] = self.user
        return {"message": "user registered successfully"}

    def verify_password(self, username, password):
        '''verify password'''
        if username in USERS:
            result = check_password_hash(USERS[username]["password"], password)
            if result is True:
                return "True"
            return {"message": "Password incorrect"}
        return {"message": "Incorrect username"}

    def reset_password(self, username):
        '''reset user password'''
        if username in USERS:
            new_password = ''.join(
                random.choice(string.ascii_uppercase + string.digits)
                for _ in range(7))
            pw_hash = generate_password_hash(new_password)
            USERS[username]["password"] = pw_hash

            return {"new_password": new_password}

        return {"message": "Incorrect username"}

    def get_all_users(self):
        '''Get all users from the users dictionary'''
        return USERS

    def get_user_by_field(self, key, value):
        '''Gets a user by a given field'''

        if self.get_all_users() is None:
            return {}
        for item in self.get_all_users().values():
            if item[key] == value:
                return item
