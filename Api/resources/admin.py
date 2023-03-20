from ..models.admin import Admin
from ..models.student import Student
from flask_restx import Namespace, fields, Resource, abort
from http import HTTPStatus
from ..models.admin import admin_required
from ..models.admin import Admin
from ..models.student import Student, default_password
from ..models.courses import Course
from ..models.registered_courses import Registeredcourses
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from ..utils import db, calculate_gpa

admin_namespace = Namespace("admin", description="The admin is responsible for managing the student management system")

student_course_model = admin_namespace.model(
    "Student_course", {
        "grade": fields.String(reqquired=True, description="a student's grade")
    }
)
student_model = admin_namespace.model(
    "PlainStudent", {
        "firstname": fields.String(required=True, description="A student's firstname"),
        "lastname": fields.String(required=True, description="A student's lastname"),
        "email": fields.String(required=True, description="A student's email address"),
        "password_hash": fields.String(required=True,
                                       description="A student's password", load_only=True),
        "student_id": fields.String(required=True,
                                    description="Students details", dump_only=True)
    }
)
reset_password_model = admin_namespace.model(
    "password", {
        "password_hash": fields.String(required=True, description="reset a student "),
        "changed_password": fields.String(required=True)
    }
)

student_model_update = admin_namespace.model(
    "StudentUpdate", {
        "firstname": fields.String(required=True, description="A student's firstname"),
        "lastname": fields.String(required=True, description="A student's lastname"),
        "email": fields.String(required=True, description="A student's email address"),
        "gpa": fields.String(required=True, description="A student's gpa"),
    }
)

registered_student_under_course = admin_namespace.model(
    "RegisteredStudentUnderCourse", {
        "id": fields.String(required=True, description="A student's ID"),
        "firstname": fields.String(required=True, description="A student's firstname"),
        "lastname": fields.String(required=True, description="A student's lastname"),
        "student_id": fields.String(required=True, description="A student's student_id"),
    }
)

admin_model = admin_namespace.model(
    "Admin", {
        "id": fields.String(required=True, description="A admin id"),
        "name": fields.String(required=True, description="An admin name"),
        "admin_id": fields.String(required=True, description="A admin_id "),
        "email": fields.String(required=True, description="A admin email"),
    }
)

student_output_model = admin_namespace.model(
    "Student", {
        "id": fields.String(required=True, description="A student's ID"),
        "firstname": fields.String(required=True, description="A student's firstname"),
        "lastname": fields.String(required=True, description="A student's lastname"),
        "email": fields.String(required=True, description="A student's email address"),
        "password_hash": fields.String(required=True, description="A student's password"),
        "gpa": fields.String(required=True, description="A student's grade point average(gpa)"),
        "date_created": fields.String(required=True, description="The date which the student was creted")
    }
)

course_model = admin_namespace.model(
    "Course", {
        "id": fields.String(required=True, description="id of the course"),
        "course_title": fields.String(required=True, description="title of the course offered"),
        "course_code": fields.String(required=True, description="code of the course offered"),
        "course_unit": fields.String(required=True, description="units of the course offered"),
        "teacher": fields.String(required=True, description="teacher of the course offered"),
        "registered_student": fields.List(fields.Nested(registered_student_under_course), description="student registered for the course", dump_only=True),
    }
)

register_a_course_model = admin_namespace.model(
    "RegisterCourse", {
        "course_title": fields.String(required=True, description="coursetitle of the course offered"),
        "course_code": fields.String(required=True, description="course code of the course offered"),
        "course_unit": fields.Integer(required=True, description="course unit of the course offered"),
        "teacher": fields.String(required=True, description="teacher of the course offered")
    })

registered_course_model = admin_namespace.model(
    "CourseRegistered", {
        "firstname": fields.String(required=True, description="firstname of the student"),
        "lastname": fields.String(required=True, description="lastname of the student"),
        "course_title": fields.String(required=True, description="coursetitle of the course offered"),
        "course_code": fields.String(required=True, description="course code of the course offered"),
        "course_unit": fields.String(required=True, description="course unit of the course offered"),
        "score": fields.String(required=True, description="score of the course offered"),
        "grade": fields.String(required=True, description="grade of the course offered"),
        "point": fields.String(required=True, description="point of the course offered")
    }
)


@admin_namespace.route('/students')
class StudentGetCreate(Resource):
    @admin_namespace.doc(description="Students lists", summary= "The lists of all Students created by the Admin" )
    @admin_namespace.marshal_list_with(student_model)
    @jwt_required()
    @admin_required
    def get(self):
        students = Student.query.all()
        
        return students, HTTPStatus.OK

    @admin_namespace.doc(description="Student creation", summary= "Adding and commiting new_students into the database" )
    @admin_namespace.expect(student_model)
    @admin_namespace.marshal_with(student_output_model)
    @jwt_required()
    @admin_required
    def post(self):
        data=admin_namespace.payload
        student = Student.query.filter_by(email=data.get("email")).first()
        if student:
            return {"message":"Student already exists"}, HTTPStatus.FORBIDDEN

        
        new_student = Student(
            firstname=data.get('firstname'), 
            lastname=data.get('lastname'), 
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password_hash')),
            gpa=data.get("gpa")
        )

        new_student.save()

        return new_student, HTTPStatus.CREATED

@admin_namespace.route('/student/<int:stud_id>')
class GetUpdateDelStudent(Resource):
    @admin_namespace.doc(description="Single student", summary= "retrieving each student using his id" )
    @admin_namespace.marshal_with(student_output_model)
    @jwt_required()
    @admin_required
    def get(self, stud_id):
        student=Student.get_by_id(stud_id)
        if student:
            return student, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message="student not found")
    

    @admin_namespace.doc(description="update student", summary= "updating and committing each student's information using his id" )
    @admin_namespace.expect(student_model_update)
    @admin_namespace.marshal_with(student_output_model)
    @jwt_required()
    @admin_required
    def patch(self, stud_id):
        student=Student.get_by_id(stud_id)

        data=admin_namespace.payload

        student.firstname=data.get("firstname")
        student.lastname=data.get("lastname")
        student.email=data.get("email")
        student.gpa=data.get("gpa")

        db.session.commit()
        
        return student, HTTPStatus.OK
    
    @admin_namespace.doc(description="delete student", summary= "deleting and committing each student's information using his id on the database" )
    @jwt_required()
    @admin_required
    def delete(self, stud_id):
        student=Student.get_by_id(stud_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return {"message": "Student has been successfully deleted" }, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message="Student does not exist")

@admin_namespace.route("/reset-student-password/string:stud_id")
class ResetPassword(Resource):
    @admin_namespace.doc(description="Password reset", summary= "Reset student password to default" )
    #@admin_namespace.expect(reset_password_model)
    @admin_namespace.marshal_with(student_output_model)
    @jwt_required()
    @admin_required
    def put(self, stud_id):
        student = Student.query.filter_by(stud_id)
        
        if student:
            student.password = default_password("registered")
            student.changed_password =False
            db.session.commit()
            return {"message: Succesfully reset password"}, HTTPStatus.OK

        else:
            abort(HTTPStatus.NOT_FOUND, message="Student not found")

        

@admin_namespace.route("/course")
class GetPostCourse(Resource):
    @admin_namespace.doc(description="course", summary= "list all courses offered" )
    @admin_namespace.marshal_list_with(course_model)
    @jwt_required()
    @admin_required
    def get(self):
        course=Course.query.all()

        return course, HTTPStatus.OK
    
    @admin_namespace.doc(description="course creation", summary= "adding and commiting a course into the database" )
    @admin_namespace.expect(register_a_course_model)
    @admin_namespace.marshal_with(register_a_course_model)
    @jwt_required()
    @admin_required
    def post(self):
        data=admin_namespace.payload
        
        if Course.query.filter_by(course_code=data.get("course_code").upper()).first():
            abort(409, message="This course already exists")

        else:

            course = Course(
                course_title=data.get("course_title").upper(),
                course_code=data.get("course_code").upper(),
                course_unit=data.get("course_unit"),
                teacher=data.get("teacher")
            )
        

            course.save()
            return course, HTTPStatus.CREATED
    
@admin_namespace.route("/course/<int:course_id>")
class GetUpdateDeleteCourse(Resource):
    @admin_namespace.doc(description="course", summary= "list all courses offered" )
    @admin_namespace.marshal_with(course_model)
    @jwt_required()
    @admin_required
    def get(self, course_id):
        course = Course.get_by_id(course_id)

        if course :
            return course, HTTPStatus.OK
        else:
            abort(HTTPStatus.CONFLICT, message="Course not found")
    

    @admin_namespace.doc(description="course update", summary= "update and commit the course in the database using the course_id" )
    @admin_namespace.expect(course_model)
    @admin_namespace.marshal_with(course_model)
    @jwt_required()
    @admin_required
    def put(self, course_id):
        course = Course.get_by_id(course_id)
        data=admin_namespace.payload()
        if course :
            course.course_title=data.get("course_title")
            course.course_code=data.get("course_code")
            course.course_unit=data.get("course_title")
            course.teacher=data.get("teacher")
            course.score=data.get("score")
            course.grade=data.get("grade")
            course.point=data.get("point")

            db.session.commit()
        
        else:
            abort(HTTPStatus.CONFLICT, message="Course not found")

    @admin_namespace.doc(description="course delete", summary= "delete and commit the course in the database using the course_id" )
    @jwt_required()
    @admin_required
    def put(self, course_id):
        course = Course.get_by_id(course_id)

        if not course :
            abort(HTTPStatus.FORBIDDEN, message="Unable to delete course")
            
        db.session.delete(course)
        db.session.commit()

        return {"message": "course has been successfully deleted"}, HTTPStatus.OK

@admin_namespace.route('/student/<int:student_id>/course/<int:course_code>/student-grade')
class GetStudentGrade(Resource):
    @admin_namespace.doc(description="student grade", summary= "get student grade using stud_id nd course_code" )
    @admin_namespace.expect(student_course_model)
    @admin_namespace.marshal_list_with(registered_course_model)
    @jwt_required()
    @admin_required
    def put(self, student_id, course_code):
        student = Student.query.filter_by(student_id=student_id)
        course= Course.query.fiter_by(course_code=course_code)
        if not student:
            abort(HTTPStatus.NOT_FOUND, message="Student not found")
        
        if not course:
            abort(HTTPStatus.NOT_FOUND, message="Course not found")
        
        registered_course = Registeredcourses.query.filter_by(student_id=student_id, course_code=course_code.upper())

        if not registered_course:
            abort(HTTPStatus.NOT_FOUND, message="Student not registered for this course")
        
        data=admin_namespace.payload
        if not data.get("grade"):
            abort(HTTPStatus.BAD_REQUEST, message="Grade cannot be left empty")
            
        registered_course.grade=data.get("grade")
        db.session.commit()
        return registered_course, HTTPStatus.OK
        
@admin_namespace.route('/student/<int:student_id>/GPA')
class GetStudentGrade(Resource):
    @admin_namespace.doc(description="Gpa Calculation", summary= "Calculation of Student Grade point Average" )
    @admin_namespace.marshal_list_with(registered_course_model)
    @jwt_required()
    @admin_required
    def patch(self, student_id):
        student = Student.query.filter_by(student_id=student_id)

        if student:
            registered_course_grades = Registeredcourses.query.filter_by(student_id=student_id). all
            grades=[record.grade for record in registered_course_grades]

            registered_course_units = Registeredcourses.query.filter_by(student_id=student_id). all
            units=[record.unit for record in registered_course_units]
            GPA= calculate_gpa(grades, units)
            student.gpa=GPA
            db.session.commit()


@admin_namespace.route('/admins')
class GetAdmin(Resource):
    @admin_namespace.doc(description="Get Admin", summary= "Get all admin registered" )
    @admin_namespace.marshal_list_with(admin_model)
    @jwt_required()
    def get(self):
        admin = Admin.query.all()

        return admin, HTTPStatus.OK

@admin_namespace.route('/admins/<int:user_id>')
class GetAdminbyID(Resource):
    @admin_namespace.doc(description="Get Admin", summary= "Get an admin using ID" )
    @admin_namespace.marshal_with(admin_model)
    @jwt_required()
    def get(self, user_id):
        admin = Admin.get_by_id(user_id)
        
        if admin:
            return admin, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, message="user is not found in the database")
