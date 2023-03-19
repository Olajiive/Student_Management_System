from flask_restx import Resource, Namespace, fields
from flask import abort
from ..models.student import Student, student_required
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from ..models.registered_courses import Registeredcourses, check_if_registered
from ..utils import db
from ..models.courses import Course

student_namespace= Namespace("student", description="Give access to the students")

student_model=student_namespace.model(
    "Student", {
        "firstname":fields.String(required=True, description="A student's firstname"),
        "lastname":fields.String(required=True, description="A student's lastname"),
        "email":fields.String(required=True, description="A student's email address"),
        "password_hash":fields.String(required=True, description="A student's password"),
        "student_id":fields.String(required=True, description="A studend_id")
    }
)

course_model = student_namespace.model(
    "Course", {
        "course_title":fields.String(required=True, description="title of thecourse offered"),
        "course_code":fields.String(required=True, description="code of the course offered"),
        "course_unit":fields.String(required=True, description="units of the course offered"),
        "teacher":fields.String(required=True, description="teacher of the course offered")
    }
)

registered_course_model = student_namespace.model(
    "Course", {
        "firstname":fields.String(required=True, description="firstname of the student"),
        "lastname":fields.String(required=True, description="lastname of the student"),
        "course_title":fields.String(required=True, description="coursetitle of the course offered"),
        "course_code":fields.String(required=True, description="course code of the course offered"),
        "course_unit":fields.String(required=True, description="course unit of the course offered"),
        "score":fields.String(required=True, description="score of the course offered"),
        "grade":fields.String(required=True, description="grade of the course offered"),
        "point":fields.String(required=True, description="point of the course offered")
    }
)


@student_namespace.route('/students/<string:email>')
class GetStudent(Resource):
    @student_namespace.doc(description="getting a student by email", summary= "Getting a student student_id so as to logged in" )
    @student_namespace.marshal_with(student_model)
    def get(self, email):
        students = Student.query.filter_by(email=email)
        if students:
            return students, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message="student not found")
    

@student_namespace.route('/student-profile')
class GetStudent(Resource):
    @student_namespace.doc(description="get a student profile", summary= "Getting a student by email provides the student details which include the student id that gives access to the student profle when logged in" )
    @student_namespace.marshal_with(student_model)
    @jwt_required()
    def get(self):
        students = Student.query.filter_by(student_id=get_jwt_identity()). first()
        
        return students, HTTPStatus.OK
    
    @student_namespace.doc(description="Update password", summary= "Updating and commiting a student password into the database " )
    @student_namespace.expect(student_model)
    @jwt_required()
    def patch(self):
        student=Student.query.filter_by(student_id=get_jwt_identity()).first
        data=student_namespace.payload

        if data.get("new_password"):
            if data.get("confirm_password"):
                if data.get("new_password") != data.get("confirm_password"):
                    abort(HTTPStatus.FORBIDDEN, message="Password does not match" )
            else:
                abort(HTTPStatus.FORBIDDEN, message="Confirm password is required")
        else:
            abort(HTTPStatus.FORBIDDEN, message="New password is required")
            
        password = generate_password_hash(data.get("password"))
        student.password = password
        student.password_changed=True
        db.session.commit()

        return {"message": "password successfully updated"}, HTTPStatus.OK

@student_namespace.route("/course")
class GetCreateCourse(Resource):
    @student_namespace.doc(description="get all courses", summary= "get all courses available  for seamless registration of course for student" )
    @student_namespace.marshal_with(course_model)
    @jwt_required()
    @student_required
    def get(self):
        course=Course.query.all()

        return course, HTTPStatus.OK
        

    @student_namespace.doc(description="course registration", summary= "Register a course using a student's identity " )
    @student_namespace.expect(course_model)
    @student_namespace.marshal_with(registered_course_model)
    @jwt_required()
    @student_required
    def post(self):
        data=student_namespace.payload

        student=Student.query.filter_by(student_id=get_jwt_identity()).first()
        course = Course.query.filter_by(course_code=data.get("course_code").upper()).first()
        
        if course:
            abort(HTTPStatus.FORBIDDEN, message="This course already exists")

        
        if not course:
            abort(HTTPStatus.NOT_FOUND, message="Course not found")

        if check_if_registered(data.get("course_code").upper()):
            abort(HTTPStatus.FORBIDDEN, message="Course has been registered already")
            
        course = Registeredcourses(
            firstname=data.get("firstname"),
            lastname=data.get("lastname"),
            course_title=data.get("course_title").upper(),
            course_code=data.get("course_code").upper(),
            course_unit=data.get("course_unit"),
            teacher=data.get("teacher"),          
            student_id=data.get("student_id")

        )

        course.save()
        return course, HTTPStatus.CREATED

@student_namespace.route("/course/<int:course_id>")
class GetPutDelete(Resource):
    @student_namespace.doc(description="get a course by id", summary= "get a course registered by a student using course_id" )
    @student_namespace.marshal_with(course_model)
    @jwt_required()
    @student_required
    def get(self, course_id):
        course=Course.get_by_id(course_id)
        if course:
            return course, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message="course not found")
        
    
    @student_namespace.doc(description="Update courses", summary= "Update registered course of a student using course_id" )
    @student_namespace.expect(registered_course_model)
    @student_namespace.marshal_with(registered_course_model)
    @jwt_required()
    @student_required
    def put(self, course_id):
        course=Registeredcourses.get_by_id(course_id)

        if course:
            course.course_title = course_id["course_title"]
            course.course_code = course_id["course_code"]
            course.course_unit= course_id["course_unit"]

            db.session.commit()
            return course, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message="course not found")
        
    
    @jwt_required()
    @student_required
    def delete(self, course_id):
        course = Course.get_by_id(course_id)

        db.session.delete(course)
        db.session.commit()

        return course, {"message": "course successfully deleted"}


        
        