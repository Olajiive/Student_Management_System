from flask_jwt_extended import create_access_token
from .. import create_app
from ..utils import db
from ..config.config import config_dict
from ..models.courses import Course
import unittest


class StudentTestCase(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = create_app(configure=config_dict['testconfig'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()
        course = Course(
                course_code="ACS202",
                course_title="ADVANCED MATHEMATHICS",
                course_unit=3,
                teacher="Olatunji"
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
            "course_code": "FBA201",
            "course_title": "MATHEMATICS FOR BUSINESS",
            "course_unit": 2,
            "teacher": "dairo",
        }

        # create JWT token for authorization
        token = create_access_token(identity="ADM|001|2023|20022")

        # set headers with JWT token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post("/create-course", json=data, headers=headers)

        self.assertEqual(response.status_code, 201)

        # check if student was created
        courses = Course.query.all()
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[1].id, 2)
        self.assertEqual(courses[1].course_unit, 2)
        self.assertEqual(courses[1].course_code, "FBA201")

    def test_all_course(self):
        course = Course.query.all()
        self.assertEqual(len(course), 1)
        self.assertEqual(course[0].id, 1)
        self.assertEqual(course[0].course_code, "ACS202")
        self.assertEqual(course[0].course_unit, 3)
        self.assertEqual(course[0].teacher, "olatunji")