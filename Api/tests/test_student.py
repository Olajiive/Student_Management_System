import unittest
from .. import create_app
from ..utils import db
from ..models.student import Student
from ..models.admin import Admin
from ..models.courses import Course
from ..models.courses import Course
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
        student= Student(
            firstname= "string",
            lastname= "string",
            email= "string",
            password_hash= pbkdf2_sha256.hash("password"),
            student_id= "STU|1010"
        )
        db.session.add(student)
        db.session.commit()

    @classmethod
    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_create_student(self):
        data = {
            "firstname": "example",
            "lastname": "example",
            "email": "string@joe.com",
            "password_hash": "string"
        }
        token = create_access_token(identity="ADM|12")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post("/admin/students", headers=headers, json=data)
        assert response.status_code == 201

    def test_get_students(self):
        token = create_access_token(identity="ADM|12")

        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get("/admin/students", headers=headers)
        assert response.status_code == 200
