import re
from flask import Flask, request, jsonify, make_response, render_template
from challenge2.main.current_user import get_logged_in_user
from challenge2.models import Questions, Answers
from challenge2.main.checker import question_already_exist, answer_already_exist
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt)
from challenge2 import models
from uuid import uuid4
from challenge2.models import ALL_QUESTIONS
#all_questions = list()
all_answers = list()


MY_QUESTION = models.Questions()
MY_USER = models.Users()

app = Flask(__name__)
app.config["TESTING"] = True
app.url_map.strict_slashes = False
app.config['JWT_SECRET_KEY'] = 'my-key'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
jwt = JWTManager(app)
BLACKLIST = set()

'''Error handlers'''




@app.route('/')
def home():
    '''method to render documentation'''
    return render_template('documentation.html'), 200


'''user actions'''


@jwt.token_in_blacklist_loader
def check_if_token_blacklist(decrypted_token):
    '''check if jti(unique identifier) is in black list'''
    json_token_identifier = decrypted_token['jti']
    return json_token_identifier in BLACKLIST


@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    '''endpoint to register a user'''
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"})
    username = data.get("username")
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if username is None or not username:
        return jsonify({"message": "Enter username"})
    if name is None or not name:
        return jsonify({"message": "Enter name"}), 206

    if len(password) < 4:
        return jsonify({"message": "password is too short"})
    if confirm_password != password:
        return jsonify({"message": "Passwords don't match"})

    match = re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match is None:
        return jsonify({"message": "Enter a valid email address"})
    response = jsonify(MY_USER.put(name, username, email, password))
    response.status_code = 201
    return response


@app.route('/api/v1/auth/login', methods=['POST'])
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


@app.route('/api/v1/auth/logout', methods=['POST'])
@jwt_required
def logout():
    '''logout user by revoking password'''
    json_token_identifier = get_raw_jwt()['jti']
    BLACKLIST.add(json_token_identifier)
    return jsonify({"message": "Successfully logged out"}), 200


@app.route('/api/v1/auth/reset-password', methods=['POST'])
def reset_password():
    '''reset user password'''
    data = request.get_json()
    if not data:
        return jsonify({"message": "Fields cannot be empty"})
    username = data.get("username")

    response = jsonify(MY_USER.reset_password(username))
    response.status_code = 200
    return response


'''question related routes'''


@app.route('/api/v1/questions', methods=['POST'])
@jwt_required
def user_post_question():
    '''user can add a question if logged in'''
    if request.method == 'POST':
        # add a question method="POST"
        data = request.get_json()
        if not data:
            return jsonify({"message": "Fields cannot be empty"})

        title = data.get('title')
        topic = data.get('topic')
        #owner = get_logged_in_user()
       # owner = "anonymous"
        details = data.get('details')
        question_id = data.get('question_id')

        if title is None or not title:
            return jsonify({"message": "Enter title"})
        if details is None or not details:
            return jsonify({"message": "Enter details for your question"})

        response = jsonify(MY_QUESTION.post_question(topic,
                                                     title,details, question_id))
        response.status_code = 200
        return response


@app.route('/api/v1/questions', methods=['GET'])
def get_all_questions():
    ''' get all questions method="GET"'''
    get_questions = MY_QUESTION.get_all()
    response = jsonify(get_questions)
    response.status_code = 200

    return response


@app.route('/api/v1/questions/<int:question_id>', methods=['GET'])
def get_question_question_id(question_id):
    '''endpoint to get question by id'''
    get_question = MY_QUESTION.get_single_question(question_id)
    response = jsonify(get_question)
    response.status_code = 200

    return response


@app.route('/api/v1/questions/<int:question_id>',
           methods=['DELETE'])
@jwt_required
def delete_question(question_id):
    '''delete a question when logged in, method=DELETE'''
    response = jsonify(MY_QUESTION.delete(question_id))
    response.status_code = 200

    return response


@app.route('/api/v1/questions/<int:question_id>/answers',
           methods=['POST'])
@jwt_required
def post_answer(question_id):
    ''' endpoint for answering a question'''
    question = MY_QUESTION.get_single_question(question_id)
    answer_body = request.json.get('answer')
    #self.question_id = request.json.get('question_id')
    if not answer_body:
        return make_response(jsonify({'message': 'Provide an answer'})), 400
    # if not question_already_exist(question_id):
        # return make_response(jsonify({'message': 'The question' +
        # ' does not exist'})), 404
    if answer_already_exist(all_answers, 'answer', answer_body):
        return make_response(jsonify(
            {'message': 'This answer is already given'})), 409
    ans_id = str(uuid4())
    answer = Answers(answer_body)
    answer_dict = answer.serialize_answer(
        ans_id, answer, question)
    all_answers.append(answer_dict)
    return make_response(jsonify({'message': 'OK'})), 200


@app.route('/api/v1/questions/<int:question_id>/' +
           'answers/<int:answer_id>', methods=['PATCH'])
@jwt_required
def accept_answer(self, question_id, answer_id):
    '''endpoint to accept an answer as your preffered'''
    answer_list = answer_already_exist(all_answers, 'ans_id', answer_id)
    if answer_list:
        if answer_list[0]['accepted']:
            return make_response(jsonify({'message': 'You have' +
                                          'already accepted'})), 409
        answer_list[0]['accepted'] = True
        return make_response(jsonify(
            {'message': 'Succesfully accepted this answer'}
        )), 200
    return make_response(jsonify({'message': 'The answer you are' +
                                  'looking for does not exist'})), 404


# method to run app.py
if __name__ == '__main__':
    app.run(debug=True)
