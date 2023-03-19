import unittest
from ..utils import db
from ..config.config import config_dict
from .. import create_app
from ..models.admin import Admin
from werkzeug.security import generate_password_hash


class UserTestCase(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.app = create_app(config_dict["testconfig"])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        admin = Admin(
            name="ola",
            email="muizolatunji29@gmail.com.com",
            admin_id="ADM|001|2023|10000",
            password=generate_password_hash("password")
        )
        db.session.add(admin)
        db.session.commit()
    @classmethod
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.app = None
        self.client = None

    def test_user_registration(self):
        # test for user registration
        data = {
            "first_name": "wonu",
            "last_name": "ola",
            "email": "wonuola@gmail.com",
            "password": "password"
        }
        response = self.client.post("/auth/signup", json=data)
        admin = Admin.query.filter_by(email=data["email"]).first()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(admin.name, data["name"])
        self.assertEqual(admin.email, data["email"])

    def test_user_login(self):
        # test for user login
        admin = Admin.query.filter_by(email="wonuola@gmail.com.com").first()
        user_id = admin.admin_id
        data = {
            "user_id": user_id,
            "password": "password"
        }
        response = self.client.post("/auth/login", json=data)
        self.assertEqual(response.status_code, 200)
