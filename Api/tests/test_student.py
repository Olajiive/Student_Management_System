import unittest
from .. import create_app
from ..utils import db
from ..models.student import Student
from ..config.config import config_dict
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash


class TestStudentProfileEndpoint(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = create_app(config_dict["testconfig"])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        # Create a test student
        student = Student(
            first_name="muiz",
            last_name="olatunji",
            email="muizolatunji29@gmail.com")
        db.session.add(student)
        db.session.commit()
    
    @classmethod
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.app = None
        self.client = None

    def test_student_profile(self):
        """Test that an authenticated student can retrieve their profile"""
        # Create an access token for the test student

        student = Student.query.filter_by(email="wonuola@gmail.com").first()
        current_user = student.stud_id
        access_token = create_access_token(identity=current_user)
        # Send a GET request to the /student-profile endpoint with the access token
        response = self.client.get("/student-profile",
                                   headers={"Authorization": f"Bearer {access_token}"})

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_update_student_password(self):
        """Test that an authenticated student can update their password"""
        # Create an access token for the test student
        student = Student.query.filter_by(email="wonuola@gmail.com").first()
        current_user = student.stud_id
        access_token = create_access_token(identity=current_user)

        # Send a PATCH request to the /student-profile endpoint with the access token and new password data
        password_data = {"new_password": "password",
                         "confirm_password": "password"}
        response = self.client.patch("/student-profile",
                                     headers={"Authorization": f"Bearer {access_token}"},
                                     json=password_data)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertTrue(generate_password_hash("newpassword", student.password_hash))