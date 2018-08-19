'''models.py containing models for the API'''
import random
import string
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
USERS = {}
ALL_QUESTIONS = {}


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


class Questions():
    '''class to represent question and answer model'''

    def __init__(self):
        self.question = {}
        self.answer = {}

    def get_all(self):
        '''return all questions from ALL_QUESTIONS dictionary'''
        return ALL_QUESTIONS

    def get_single_question(self, question_id):
        '''get single question from ALL_QUESTIONS using id'''
        if question_id in ALL_QUESTIONS:
            return ALL_QUESTIONS[question_id]

        return {"message": "Question not found"}

    def post_question(self, topic, title, details, question_id=None):
        '''add a question to ALL_QUESTIONS'''
        if title in ALL_QUESTIONS:
            return {"message": "Question  entered already exists"}

        self.question["title"] = title
        #self.question["owner"] = owner
        self.question["details"] = details
        self.question["topic"] = topic

        ALL_QUESTIONS[question_id] = self.question
        return {"message": "Question added successfully"}

    # delete question

    def delete(self, question_id):
        '''delete a question by its id'''
        if question_id in ALL_QUESTIONS:
            del ALL_QUESTIONS[question_id]
            return {"message": "Question {} deleted successfully"
                    .format(question_id)}

        return {"message": "Question you are trying to delete doesn't exist"}


class Answers():
    '''answer class conaining answer related operations'''

    def __init__(self, answer_body):
        '''constructor method to initialize an object'''
        self.answer_body = answer_body
        self.answer_id = str(uuid4())

    def serialize_answer(self, ans_id, answer_body, question):
        '''take answer object and return __dict__ representation'''
        return dict(
            answer=self.answer_body,
            ans_id=self.answer_id,
            accepted=False,
            question=question
        )
