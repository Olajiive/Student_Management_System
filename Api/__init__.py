from flask import Flask, jsonify
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
from .blocklist import BLOCKLIST


def create_app(config=config_dict["devconfig"]):
    app = Flask(__name__) 

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)
    jwt=JWTManager(app)

    api=Api(app)

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 405
    


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )
    @jwt.additional_claims_loader
    def add_additional_claims(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )
    # this is going to check the BLOCKLIST set if the token you're trying to use exist in the set
    # if the token is present in the set, it will return a 'token revoked' message
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    api.add_namespace(admin_namespace, path="/admin")
    api.add_namespace(student_namespace, path="/student")
    api.add_namespace(auth_namespace, path="/auth")
    
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