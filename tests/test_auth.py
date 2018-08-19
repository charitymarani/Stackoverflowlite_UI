import unittest
import json
import ast
from Stackoverflowlite import app
from Stackoverflowlite.app import all_answers
from Stackoverflowlite.models import USERS
from Stackoverflowlite.models import ALL_QUESTIONS


class TestAuthEndpoints(unittest.TestCase):
    '''class to tests app.py'''

    def setUp(self):
        '''create a test client'''
        with app.app.app_context():
            self.client = app.app.test_client
            self.question = {"question_id": 23, "topic": "java",
                             "title": "What is java", "details": "",
                             "answers": [{"1": "Java is an oop language"},
                                         {"1": "Java is an oop language"},
                                         {"1": "Java is an oop language"}]
                             }

    def tearDown(self):
        '''clear list data for every test case to be atomic'''
        del all_answers[:]
        ALL_QUESTIONS.clear()
        USERS.clear()


class TestUserActions(TestAuthEndpoints):
    def test_user_register(self):
        '''method to test register, login and logout endpoints'''
        # test register
        result = self.client().post('/api/v1/auth/register',

                                    content_type='application/json',
                                    data=json.dumps({"username": "hawa",
                                                     "name": "Hawaii Yusuf",
                                                     "email": "hawa@gmail.com",
                                                     "password": "where",
                                                     "confirm_password":
                                                     "where"}))
        self.assertEqual(result.status_code, 201)
        # self.assertEqual(result["message"], "user registered successfully")
        print(result.data)
        self.assertIn("user registered successfully", str(result.data))

    def test_user_login(self):
        # test login
        result = self.client().post('/api/v1/auth/register',

                                    content_type='application/json',
                                    data=json.dumps({"username": "hawa",
                                                     "name": "Hawaii Yusuf",
                                                     "email": "hawa@gmail.com",
                                                     "password": "where",
                                                     "confirm_password":
                                                     "where"}))
        self.assertEqual(result.status_code, 201)
        result2 = self.client().post('/api/v1/auth/login',
                                     content_type='application/json',
                                     data=json.dumps({"username": "hawa",
                                                      "password": "where"}))

        my_data = ast.literal_eval(result2.data.decode())
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        print(result2.data)
        self.assertEqual("Login successful", my_data["message"])

    def test_post_question(self):
        # post_question
         # test login
        result = self.client().post('/api/v1/auth/register',

                                    content_type='application/json',
                                    data=json.dumps({"username": "hawa",
                                                     "name": "Hawaii Yusuf",
                                                     "email": "hawa@gmail.com",
                                                     "password": "where",
                                                     "confirm_password":
                                                     "where"}))
        self.assertEqual(result.status_code, 201)
        result2 = self.client().post('/api/v1/auth/login',
                                     content_type='application/json',
                                     data=json.dumps({"username": "hawa",
                                                      "password": "where"}))

        my_data = ast.literal_eval(result2.data.decode())
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        print(result2.data)
        self.assertEqual("Login successful", my_data["message"])
        response = self.client().post(
            '/api/v1/questions',
            headers=dict(
                Authorization='Bearer ' + a_token
            ),
            data=json.dumps(dict(
                topic='python',
                question_id=1,
                details='I do not seem to understand jwt,what is it where  is it use',
                title='What is token based authentication?'
            )),
            content_type='application/json'
        )
        response_data = ast.literal_eval(response.data.decode())
        print(response.data)
        self.assertTrue(response_data['message'] ==
                        'Question added successfully')
        self.assertEqual(response.status_code, 200)

    def test_post_answer(self):
        result = self.client().post('/api/v1/auth/register',

                                    content_type='application/json',
                                    data=json.dumps({"username": "hawa",
                                                     "name": "Hawaii Yusuf",
                                                     "email": "hawa@gmail.com",
                                                     "password": "where",
                                                     "confirm_password":
                                                     "where"}))
        self.assertEqual(result.status_code, 201)
        result2 = self.client().post('/api/v1/auth/login',
                                     content_type='application/json',
                                     data=json.dumps({"username": "hawa",
                                                      "password": "where"}))

        my_data = ast.literal_eval(result2.data.decode())
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        print(result2.data)
        self.assertEqual("Login successful", my_data["message"])
        response = self.client().post(
            '/api/v1/questions',
            headers=dict(
                Authorization='Bearer ' + a_token
            ),
            data=json.dumps(dict(
                topic='python',
                question_id=1,
                details='I do not seem to understand jwt,what is it where  is it use',
                title='What is token based authentication?'
            )),
            content_type='application/json'
        )
        response_data = ast.literal_eval(response.data.decode())
        print(response.data)
        self.assertTrue(response_data['message'] ==
                        'Question added successfully')
        self.assertEqual(response.status_code, 200)
        # post answer
        resp = self.client().post('/api/v1/questions/1/answers',
                                  headers=dict(
                                      Authorization='Bearer ' + a_token),
                                  data=json.dumps(dict(
                                      ans_id=2,

                                      answer='the answer is this and that'
                                  )),
                                  content_type='application/json'
                                  )
        response_data = ast.literal_eval(resp.data.decode())
        print(resp)
        self.assertTrue(response_data['message'] ==
                        'OK')
        self.assertEqual(resp.status_code, 200)

    def test_get_all_questions(self):
        # get all questions
        result = self.client().post('/api/v1/auth/register',

                                    content_type='application/json',
                                    data=json.dumps({"username": "hawa",
                                                     "name": "Hawaii Yusuf",
                                                     "email": "hawa@gmail.com",
                                                     "password": "where",
                                                     "confirm_password":
                                                     "where"}))
        self.assertEqual(result.status_code, 201)
        result2 = self.client().post('/api/v1/auth/login',
                                     content_type='application/json',
                                     data=json.dumps({"username": "hawa",
                                                      "password": "where"}))

        my_data = ast.literal_eval(result2.data.decode())
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        print(result2.data)
        self.assertEqual("Login successful", my_data["message"])
        response = self.client().post(
            '/api/v1/questions',
            headers=dict(
                Authorization='Bearer ' + a_token
            ),
            data=json.dumps(dict(
                topic='python',
                question_id=1,
                details='I do not seem to understand jwt,what is it where  is it use',
                title='What is token based authentication?'
            )),
            content_type='application/json'
        )
        response_data = ast.literal_eval(response.data.decode())
        print(response.data)
        self.assertTrue(response_data['message'] ==
                        'Question added successfully')
        self.assertEqual(response.status_code, 200)
        """Test that a user can get all the questions(GET request)"""
        new_quest = self.client().post('/api/v1/questions',
                                       headers=dict(
                                           Authorization='Bearer ' + a_token
                                       ),
                                       data=json.dumps(self.question),
                                       content_type='application/json')
        self.assertEqual(new_quest.status_code, 200)
        response = self.client().get('/api/v1/questions')
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_question_by_id(self):
        # get question by id
        result = self.client().post('/api/v1/auth/register',

                                    content_type='application/json',
                                    data=json.dumps({"username": "hawa",
                                                     "name": "Hawaii Yusuf",
                                                     "email": "hawa@gmail.com",
                                                     "password": "where",
                                                     "confirm_password":
                                                     "where"}))
        self.assertEqual(result.status_code, 201)
        result2 = self.client().post('/api/v1/auth/login',
                                     content_type='application/json',
                                     data=json.dumps({"username": "hawa",
                                                      "password": "where"}))

        my_data = ast.literal_eval(result2.data.decode())
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        print(result2.data)
        self.assertEqual("Login successful", my_data["message"])
        response = self.client().post(
            '/api/v1/questions',
            headers=dict(
                Authorization='Bearer ' + a_token
            ),
            data=json.dumps(dict(
                topic='python',
                question_id=1,
                details='I do not seem to understand jwt,what is it where  is it use',
                title='What is token based authentication?'
            )),
            content_type='application/json'
        )
        response_data = ast.literal_eval(response.data.decode())
        print(response.data)
        self.assertTrue(response_data['message'] ==
                        'Question added successfully')
        self.assertEqual(response.status_code, 200)
        response = self.client().get(
            '/api/v1/questions/1')
        # check that the server responds with the correct status code
        self.assertEqual(response.status_code, 200)
        print(response.data)
        # test that the response contains the correct question
        self.assertIn("What is token based authentication?",
                      str(response.data))
        # delete question
        res = self.client().delete('/api/v1/questions/23',
                                   headers=dict(
                                       Authorization='Bearer ' + a_token))

        self.assertEqual(res.status_code, 200)
        # test to check whether deleted item exists
        result = self.client().get('/api/v1/questions/23')
        self.assertIn("Question not found", str(result.data))

    def test_logout(self):
        # test logout
        result = self.client().post('/api/v1/auth/register',

                                    content_type='application/json',
                                    data=json.dumps({"username": "hawa",
                                                     "name": "Hawaii Yusuf",
                                                     "email": "hawa@gmail.com",
                                                     "password": "where",
                                                     "confirm_password":
                                                     "where"}))
        self.assertEqual(result.status_code, 201)
        result2 = self.client().post('/api/v1/auth/login',
                                     content_type='application/json',
                                     data=json.dumps({"username": "hawa",
                                                      "password": "where"}))

        my_data = ast.literal_eval(result2.data.decode())
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        print(result2.data)
        self.assertEqual("Login successful", my_data["message"])
        result4 = self.client().post('/api/v1/auth/logout',
                                     headers=dict(Authorization="Bearer " +
                                                  a_token))
        self.assertEqual(result4.status_code, 200)
        self.assertIn('Successfully logged out', str(result4.data))

    def test_reset_password(self):
        '''test reset password method = ("POST")'''
        result = self.client().post('/api/v1/auth/register',
                                    content_type='application/json',
                                    data=json.dumps({"username": "lucy",
                                                     "name": "Morningstar",
                                                     "email": "lucy@gmail.com",
                                                     "password": "1234",
                                                     "confirm_password":
                                                     "1234"}))
        self.assertEqual(result.status_code, 201)

        result2 = self.client().post('/api/v1/auth/reset-password',
                                     content_type="application/json",
                                     data=json.dumps({"username": "lucy"}))
        self.assertEqual(result2.status_code, 200)


if __name__ == "__main__":
    unittest.main()
