import unittest
from .. import create_app
from ..utils import db
from ..models.student import Student
from ..models.admin import Admin
from ..config.config import config_dict
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256


class TestStudentByAdmin(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = create_app(config=config_dict["testconfig"])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()
        admin = Admin(
            name="muiz",
            email="muizolatunji29@gmail.com",
            admin_id="ADM|002|2023|11001",
            password_hash=pbkdf2_sha256.hash("password")
        )
        db.session.add(admin)
        db.session.commit()

    @classmethod
    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_register(self):
        data = {
            "name": "micheal",
            "email": "joe@example.com",
            "password_hash": "password"
        }
        response = self.client.post("/auth/signup", json=data)
        assert response.status_code == 201

    def test_login(self):
        data = {
            "user_id": "ADM|002|2023|11001",
            "password_hash": "password"
        }

        response = self.client.post("/auth/login", json=data)
        assert response.status_code == 200
