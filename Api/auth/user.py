from flask_restx import Namespace,Resource, fields, abort
from flask import request
from ..models.admin import Admin
from ..models.student import Student
from flask_jwt_extended import create_access_token,\
    create_refresh_token,jwt_manager, get_jwt, get_jwt_identity, jwt_required
# from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from datetime import timedelta
from ..blocklist import BLOCKLIST
from passlib.hash import pbkdf2_sha256

# create an instance of the namespace from flask_restx
auth_namespace=Namespace("auth", description="Aunthentication of users")

signup_model=auth_namespace.model(
    "Signup", {
    "name":fields.String(required=True, description="name of the admin"),
    "email":fields.String(required=True, description="email of the admin"),
    "password_hash":fields.String(required=True, description="password of the admin")
    }
)

signup_output_model=auth_namespace.model(
    "Signup_Output", {
    "admin_id":fields.String(required=True, description="Unique id of the admin"),
    "name":fields.String(required=True, description="name of the admin"),
    "email":fields.String(required=True, description="email of the admin"),
    "password_hash":fields.String(required=True, description="password of the admin")
    }
)

login_model=auth_namespace.model(
    "Login", {
    "user_id":fields.String(required=True, description="user's id"),
    "password_hash":fields.String(required=True, description="password of the user")
    }
)

@auth_namespace.route("/signup")
class Signup(Resource):
    @auth_namespace.doc(description="Signup a user", summary="Signup a  new user")
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_output_model)
    def post(self):

        data=request.get_json()
        reg_admin=Admin.query.filter(Admin.email==data.get('email').lower()).first()

        if reg_admin :
            #if the details provided by the user already exists in the database, abort the registration process with HTTPStatus.CONFLICT
            abort(HTTPStatus.CONFLICT, message="A user with the entered details already exists.")


        #if the user details has not been initially created in the database,then commit the user into the database

        new_admin =Admin(name=data.get('name'),
                         email=data.get('email'),
                         password_hash=pbkdf2_sha256.hash(data.get('password_hash'))
                        )
        new_admin.save()

        return new_admin, HTTPStatus.CREATED

    
@auth_namespace.route("/login")
class Login(Resource):
    @auth_namespace.doc(description="Login a user",
                        summary="login a user after providing valid login details" )
    @auth_namespace.expect(login_model)
    # @auth_namespace.marshal_with(login_model)
    def post(self):
        # data=request.get_json()
        data = auth_namespace.payload

        if data.get('user_id').startswith('ADM|'):
            user_id=data.get("user_id")
            admin = Admin.query.filter(Admin.admin_id == user_id).first()

            if admin:
                if pbkdf2_sha256.verify(data.get("password_hash"), admin.password_hash):
                    access_token = create_access_token(identity=user_id, expires_delta=timedelta(minutes=30))
                    refresh_token=create_refresh_token(identity=user_id, expires_delta=timedelta(days=30))
                    response = {
                        "access_token":access_token,
                        "refresh_token":refresh_token

                    }
                    return response, HTTPStatus.OK
                else:
                    abort(500, message="wrong password")
            else:
                abort(404, message="wrong user id")

        elif data.get('user_id').startswith('STU'):
            email=data.get("email")
            student =Student.query.filter(Student.email == data.get("email")).first()

            if student:
                if pbkdf2_sha256.verify(data.get("password_hash"), student.password_hash) :
                    access_token = create_access_token(identity=student.student_id)
                    refresh_token=create_refresh_token(identity=student.student_id)

                    response = {
                        "create_access_token":access_token,
                        "create_refresh_token":refresh_token

                    }
                    return response, HTTPStatus.OK
                else:
                    abort(500, message="wrong password b")
            else:
                abort(404, message="Student not found")
        else:
            abort(404, message="wrong credentials")
        
        
       
        # return abort(HTTPStatus.NOT_FOUND, message="User not found")
    
auth_namespace.route('/refresh')
class TokenRefresh(Resource):
    @auth_namespace.doc(description="Refresh an access token", summary="Refresh an access token using a refresh token")
    @jwt_required(refresh=True)
    def post(self):
        current_user=get_jwt_identity

        new_token=create_access_token(current_user, expires_data=timedelta(minutes=45))

        return {"access_token": new_token}
        

auth_namespace.route('/logout')
class Logout(Resource):
    @auth_namespace.doc(description="Logout a registered user", summary="Logout a registered user after providing an access token")
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)

        return {"access_token": "successfully logged user out"}
           

