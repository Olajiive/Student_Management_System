import unittest
from .. import create_app
from ..utils import db
from ..models.student import Student
from ..config.config import config_dict
from flask_jwt_extended import create_access_token


class TestStudentByAdmin(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = create_app(configure=config_dict['testconfig'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()
        student = Student(
            first_name="muiz",
            last_name="olatunji",
            email="muizolatunji29@gmail.com",
            stud_id="STU|002|2023|11001"
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
            "first_name": "tolu",
            "last_name": "adebayo",
            "email": "toluadebayo@gmail.com"
        }

        # create JWT token for authorization
        token = create_access_token(identity="ADM|002|2023|10011")

        # set headers with JWT token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post("/create-student", json=data, headers=headers)

        self.assertEqual(response.status_code, 201)

        # check if student was created
        students = Student.query.all()
        self.assertEqual(len(students), 2)
        self.assertEqual(students[1].id, 2)
        self.assertEqual(students[1].first_name, "taiwo")
        self.assertEqual(students[1].last_name, "ademola")
        self.assertTrue(students[1].student_id.startswith("STU"))

    def test_get_students(self):
        # create JWT token for authorization
        token = create_access_token(identity="ADM|001|2023|10200")

        # set headers with JWT token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get("/students", headers=headers)
        self.assertEqual(response.status_code, 200)
        students = Student.query.all()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].courses_registered, [])

    def test_update_student(self):

        student = Student.query.filter_by(email="olawunmi44@gmail.com").first()
        stud_id = student.stud_id

        token = create_access_token(identity="ADMIN-2023-020200")

        # set headers with JWT token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.put(f"/student/{stud_id}",
                                   headers=headers,
                                   json={
                                    "first_name": "ade",
                                    "last_name": "",
                                    "email": ""
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(student.first_name, 'ade')
        self.assertEqual(student.email, 'adefeso@gmail.com')

    def test_each_student(self):
        student = Student.query.filter_by(email="adefeso@gmail.com").first()
        stud_id = student.stud_id

        token = create_access_token(identity="ADM|001|2023|10111")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get(f"/student/{stud_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['firstname'], 'adefeso')
