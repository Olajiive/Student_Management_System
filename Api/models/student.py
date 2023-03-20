from ..utils import db
from datetime import datetime
from functools import wraps
from flask_restx import abort
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash
from http import HTTPStatus
from ..code_gen import  code_generator

class Student(db.Model):
    __tablename__ = "students"
    id=db.Column(db.Integer(), primary_key=True)
    firstname=db.Column(db.String(), nullable=False)
    lastname=db.Column(db.String(), nullable=False)
    student_id=db.Column(db.String(70), unique=True, nullable=False,
                         default=code_generator(f"STU|002|{datetime.now().year}|"))
    email=db.Column(db.String(150), unique=True, nullable=False)
    password_hash=db.Column(db.Text(), nullable=False)
    gpa=db.Column(db.Float(), default=0.00, nullable=False)
    date_created=db.Column(db.DateTime(), default=datetime.utcnow)
    changed_password=db.Column(db.Boolean, default=False)
    courses_registered=db.relationship("Registeredcourses", backref="student", lazy=True)


    def __repr__(self) -> str:
        return f"<Student {self.id}>"
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

def default_password(default_password):
    password=generate_password_hash(default_password)
    return password

def student_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user= get_jwt_identity()
        if not user.startswith("STU"):
            abort(HTTPStatus.UNAUTHORIZED, message="Restricted to only a student")
        
        return func(*args, **kwargs)
    return wrapper
        