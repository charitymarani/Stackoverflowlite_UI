import unittest
import os
import json
import ast
from app.api.v1.question.views import all_questions
from app.api.v1.question.views import all_answers
from app import createapp


class TestDefault(unittest.TestCase):
    """test base class"""

    def setUp(self):
        """Create a test client"""
        self.app = createapp.APP
        self.client = self.app.test_client
        self.question = {"question_id": 23, "topic": "java",
                         "title": "What is java", "details": "",
                         "answers": [{"1": "Java is an oop language"},
                                     {"1": "Java is an oop language"},
                                     {"1": "Java is an oop language"}]
                         }

    def tearDown(self):
        '''empty list after each test case'''
        del all_questions[:]
        del all_answers[:]


class TestQuestions(TestDefault):
    """Class to test endpoints  relate dto questions"""

    def test_api_can_get_all_questions(self):
        """Test that a user can get all the questions(GET request)"""
        new_quest = self.client().post('/api/v1/questions/',
                                       data=json.dumps(self.question),
                                       content_type='application/json')
        self.assertEqual(new_quest.status_code, 201)
        response = self.client().get('/api/v1/questions')
        self.assertEqual(response.status_code, 200)

    def test_api_can_get_question_by_id(self):
        """Test that the API retrieve a question by id"""
        # post a new question to get a question id in the response
        new_question = self.client().post('/api/v1/questions/',
                                          data=json.dumps(self.question),
                                          content_type='application/json')
        self.assertEqual(new_question.status_code, 201)
        response = self.client().get(
            '/api/questions/23')
        # check that the server responds with the correct status code
        self.assertEqual(response.status_code, 200)
        print(response.data)
        # test that the response contains the correct question
        self.assertIn("What is java", str(response.data))

    def test_post_question(self):
         # register
        self.client().post('/api/v1/auth/register/',
                           data=json.dumps(dict(
                               name='val',
                               email='v@gmail.com',
                               username='vma',
                               password='shegoat')),
                           content_type='application/json'
                           )
        # test login
        result2 = self.client().post('/api/v1/auth/login/',
                                     content_type='application/json',
                                     data=json.dumps({'username': 'vma',
                                                      'password': 'shegoat'}))
        my_data = ast.literal_eval(result2.data)
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        self.assertEqual("Login successful", my_data["message"])
        response = self.client().post(
            '/api/v1/questions',
            headers=dict(
                Authorization='Bearer ' + a_token
            ),
            data=json.dumps(dict(
                title='python',
                description='What is token based authentication?'
            )),
            content_type='application/json'
        )
        response_data = ast.literal_eval(response.data)
        self.assertTrue(response_data['message'] ==
                        'Posted question successfully')
        self.assertEqual(response.status_code, 201)

    def test_api_can_delete_question(self):
        '''test that api can delete question (DELETE request)'''
        # first register a user

        self.client().post('/api/v1/auth/register/',
                           data=json.dumps(dict(
                               name='hey',
                               email='hey@gmail.com',
                               username='heyma',
                               password='shegoat')),
                           content_type='application/json'
                           )
        # test login
        result2 = self.client().post('/api/v1/auth/login/',
                                     content_type='application/json',
                                     data=json.dumps({'username': 'heyma',
                                                      'password': 'shegoat'}))
        my_data = ast.literal_eval(result2.data)
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        self.assertEqual("Login successful", my_data["message"])
        # post question
        response = self.client().post('/api/v1/questions/',
                                      headers=dict(
                                          Authorization='Bearer ' + a_token),
                                      data=json.dumps(dict(
                                          question_id=16,
                                          title='python',
                                          description='What is token based' +
                                          'authentication?')),
                                      content_type='application/json')
        response_data = ast.literal_eval(response.data)
        self.assertTrue(response_data['message'] ==
                        'Posted question successfully')
        self.assertEqual(response.status_code, 201)
        # delete the question you posted
        res = self.client().delete('/api/v1/questions/16',
                                   headers=dict(
                                       Authorization='Bearer ' + a_token))

        self.assertEqual(res.status_code, 200)
        # test to check whether deleted item exists
        result = self.client().get('/api/v1/questions/23')
        self.assertIn("Question not found", result.data)

    def test_post_answer(self):
                # first register a user

        self.client().post('/api/v1/auth/register/',
                           data=json.dumps(dict(
                               name='joy',
                               email='j@gmail.com',
                               username='joma',
                               password='shegoat')),
                           content_type='application/json'
                           )
        # test login
        result2 = self.client().post('/api/v1/auth/login/',
                                     content_type='application/json',
                                     data=json.dumps({'username': 'joma',
                                                      'password': 'shegoat'}))
        my_data = ast.literal_eval(result2.data)
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        self.assertEqual("Login successful", my_data["message"])
        resp = self.client().post('/api/v1/questions/1/answers/',
                                  headers=dict(
                                      Authorization='Bearer ' + a_token),
                                  data=json.dumps(dict(
                                      answer='the answer is this and that'
                                  )),
                                  content_type='application/json'
                                  )
        response_data = ast.literal_eval(resp.data)

        self.assertTrue(response_data['message'] ==
                        'Answer posted successfully')
        self.assertEqual(resp.status_code, 201)

    def accept_answer(self):
        # first register a user

        self.client().post('/api/v1/auth/register/',
                           data=json.dumps(dict(
                               name='Charo',
                               email='charo@gmail.com',
                               username='chama',
                               password='shegoat')),
                           content_type='application/json'
                           )
        # test login
        result2 = self.client().post('/api/v1/auth/login/',
                                     content_type='application/json',
                                     data=json.dumps({'username': 'chama',
                                                      'password': 'shegoat'}))
        my_data = ast.literal_eval(result2.data)
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        self.assertEqual("Login successful", my_data["message"])
        resp = self.client().post('/api/v1/questions/1/answers',
                                  headers=dict(
                                      Authorization='Bearer ' + a_token),
                                  data=json.dumps(dict(
                                      answer='the answer is this and that',
                                      ans_id=1)),
                                  content_type='application/json')
        response_data = ast.literal_eval(resp.data)

        self.assertTrue(response_data['message'] ==
                        'Answer posted successfully')
        self.assertEqual(resp.status_code, 201)
        ac_resp = self.client().patch('/api/v1/questions/1/answers/1/accept/',
                                      headers=dict(
                                          Authorization='Bearer ' + a_token),
                                      data=json.dumps(dict(
                                          accepted=True)),
                                      content_type='application/json')
        respo_data = ast.literal_eval(ac_resp.data)
        print(respo_data)

        self.assertTrue(response_data['message'] == 'Answer accepted')
        self.assertEqual(ac_resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
