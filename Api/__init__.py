from flask import Flask
from .utils import db
from flask_restx import Api
from .config.config import config_dict
from .auth.user import auth_namespace
from .resources.admin import admin_namespace
from .resources.student import student_namespace
from .models.admin import Admin
from .models.student import Student
from .models.courses import Course
from .models.registered_courses import Registeredcourses
from werkzeug.exceptions import NotFound, MethodNotAllowed
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


def create_app(config=config_dict["devconfig"]):
    app = Flask(__name__) 

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)
    JWTManager(app)

    api=Api(app)

    api.add_namespace(admin_namespace, path="/admin")
    api.add_namespace(student_namespace, path="/student")
    api.add_namespace(auth_namespace, path="/auth")

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 405
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "admin":Admin,
            "students":Student,
            "courses":Course,
            "registeredcourse":Registeredcourses
        }
    return app