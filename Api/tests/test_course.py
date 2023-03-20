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
        course= Course(
            course_title= "string111",
            course_code= "string111",
            course_unit= 3,
            teacher= "johnson"
        )
        db.session.add(course)
        db.session.commit()

    @classmethod
    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_create_course(self):
        data = {
            "course_title": "string111",
            "course_code": "string111",
            "course_unit": 3,
            "teacher": "johnson"
        }
        token = create_access_token(identity="ADM|12")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post("/admin/course", headers=headers, json=data)
        assert response.status_code == 201

    def test_get_all_courses(self):
        token = create_access_token(identity="ADM|12")

        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get("/admin/course", headers=headers)
        assert response.status_code == 200
        courses = Course.query.all()
        assert courses != []
        assert len(courses) == 1

    def test_get_a_course(self):
        token = create_access_token(identity="ADM|12")

        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get("/admin/course/1", headers=headers)
        assert response.status_code == 200
