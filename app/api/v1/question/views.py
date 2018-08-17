'''question views '''
from flask import make_response, jsonify, request, Blueprint
from app.api.v1.main.checker import already_exist
from app.api.v1.question.question_model import Questions, Answers
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt)
from app.api.v1.auth import auth_model
from app.api.v1.question import question_model
from app.current_user import get_logged_in_user
from uuid import uuid4

all_questions = list()
qn = Blueprint('question', __name__)
all_answers = list()
MY_USER = auth_model.Users()
MY_QUESTION = question_model.Questions()

@qn.route('/api/v1/questions', methods=['POST'])
@jwt_required
def user_post_question():
    '''user can add a question if logged in'''
    if request.method == 'POST':
        # add a question method="POST"
        data = request.get_json()
        if not data:
            return jsonify({"message": "Fields cannot be empty"})

        title = (data.get('title')).strip()
        owner = get_logged_in_user()
        details = (data.get('details')).strip()
        question_id = data.get('question_id')
        answers = (data.get('answers')).strip()

        if title is None or not title:
            return jsonify({"message": "Enter title"})
        if details is None or not details:
            return jsonify({"message": "Enter details for your question"})

        response = jsonify(MY_QUESTION.post_question(
            title, owner, details, question_id, answers))
        response.status_code = 200
        return response


@qn.route('/api/v1/questions', methods=['GET'])
def get_all_questions():
    ''' get all questions method="GET"'''
    get_questions = MY_QUESTION.get_all()
    response = jsonify(get_questions)
    response.status_code = 200

    return response


@qn.route('/api/v1/questions/<int:question_id>', methods=['GET'])
def get_question_question_id(question_id):
    '''endpoint to get question by id'''
    get_question = MY_QUESTION.get_single_question(question_id)
    response = jsonify(get_question)
    response.status_code = 200

    return response


@qn.route('/api/v1/questions/<int:question_id>',
          methods=['DELETE'])
@jwt_required
def delete_question(question_id):
    '''delete a question when logged in, method=DELETE'''
    response = jsonify(MY_QUESTION.delete(question_id))
    response.status_code = 200

    return response


@qn.route('/api/v1/questions/<int:question_id>/answers',
          methods=['POST'])
@jwt_required
def post_answer(self, questionId):
    ''' endpoint for answering a question'''
    answer_body = request.json.get('answer')
    if not answer_body:
        return make_response(jsonify({'mesage': 'Provide an answer'})), 400
    if not already_exist(all_questions, 'questionId', int(questionId)):
        return make_response(jsonify({'message': 'The question' +
                                      'does not exist'})), 404
    if already_exist(all_answers, 'answer', answer_body):
        return make_response(jsonify(
            {'message': 'This answer is already given'})), 409
    ans_id = str(uuid4())
    answer = Answers(answer_body)
    answer_dict = answer.serialize_answer(
        ans_id, questionId)
    all_answers.append(answer_dict)
    return make_response(jsonify({'message': 'Succesfully posted the' +
                                  'answer'})), 201


@qn.route('/api/v1/questions/<int:question_id>/' +
          'answers/<int:answer_id>', methods=['PATCH'])
def accept_answer(self, questionId, answerId):
    '''endpoint to accept an answer as your preffered'''
    answer_list = already_exist(all_answers, 'answerId', int(answerId))
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
