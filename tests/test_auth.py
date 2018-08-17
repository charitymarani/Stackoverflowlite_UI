import unittest
import json
import ast
import app
from app import create_app
from app.api.v1.auth import views
from config import CONFIG
from app.api.v1.auth import auth_model
from app.api.v1.auth.views import BLACKLIST
from app.api.v1.auth.auth_model import USERS


class TestAuthEndpoints(unittest.TestCase):
    '''class to tests auth.views.py'''

    def setUp(self):
        """Create a test client"""
        self.app = create_app('testing')
        self.client = self.app.test_client

    def test_user_actions(self):
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
        self.assertIn("user registered successfully", result.data)

        # test login
        result2 = self.client().post('/api/v1/auth/login',
                                     content_type='application/json',
                                     data=json.dumps({"username": "hawa",
                                                      "password": "where"}))
        my_data = ast.literal_eval(result2.data)
        a_token = my_data["token"]
        self.assertEqual(result2.status_code, 200)
        self.assertEqual("Login successful", my_data["message"])

        # test logout
        result4 = self.client().post('/api/v1/auth/logout',
                                     headers=dict(Authorization="Bearer " +
                                                  a_token))
        self.assertEqual(result4.status_code, 200)
        self.assertIn('Successfully logged out', result4.data)

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
