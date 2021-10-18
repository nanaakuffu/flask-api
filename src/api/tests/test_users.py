import json
from datetime import datetime
import unittest2 as unittest

from src.api.utils.test_base import BaseTestCase
from ..resources.models import User
from ..utils.token import generateVerificationToken, confirmVerificationToken


def create_users():
    user1 = User(email="kunal.relan12@gmail.com",
                 username='kunalrelan12',
                 password=User.generateHash('helloworld'),
                 isVerified=True
                 ).create()

    user2 = User(email="kunal.relan123@gmail.com",
                 username='kunalrelan125',
                 password=User.generateHash('helloworld')
                 ).create()


class TestUsers(BaseTestCase):
    def setUp(self) -> None:
        super(TestUsers, self).setUp()
        create_users()

    def test_login_user(self):
        user = {
            "email": "kunal.relan12@gmail.com",
            "password": "helloworld"
        }

        response = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(user),
            content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('token' in data)


if __name__ == '__main__':
    unittest.main()
