import unittest
from api import create_app
from ..config.config import config_dict
from ..models.users import User
from ..utils import db


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app=create_app(config=config_dict['test'])

        self.appctx=self.app.app_context()

        self.appctx.push()

        self.client=self.app.test_client()

        db.create_all()


    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app=None

        self.client =None


    def test_user_registration(self):

        data={
            "username":"testuser",
            "email":"testuser@company.com",
            "password":"password"
        }

        response=self.client.post('/auth/signup',json=data)

        user=User.query.filter_by(email="testuser@company.com").first()

        assert user.username == "testuser"


        assert response.status_code == 201


    def test_login(self):

        data={
            "email":"testuser@company.com",
            "password":"password"
        }

        response=self.client.post('/auth/login',json=data)


        assert response.status_code == 200