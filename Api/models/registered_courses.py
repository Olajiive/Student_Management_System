from ..utils import db
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from ..code_gen import code_generator

class Registeredcourses(db.Model):
    __tablename__= "registered_course"
    id = db.Column(db.Integer(), primary_key=True)
    firstname=db.Column(db.String(), nullable=False)
    lastname=db.Column(db.String(), nullable=False)
    course_title=db.Column(db.String(), nullable=False)
    course_code=db.Column(db.String(), nullable=False)
    course_unit=db.Column(db.Integer(), nullable=False)
    score = db.Column(db.Integer(), nullable=False)
    grade = db.Column(db.String(), nullable=False)
    point = db.Column(db.Integer(), nullable=False )
    student_id=db.Column(db.String(70), unique=True, nullable=False, default=code_generator(f"STU|002|{datetime.now().year}|"))
    stud_id =db.Column(db.Integer(), db.ForeignKey("students.id"))
    course_id=db.Column(db.Integer(), db.ForeignKey("courses.id"))
    
    def __repr__(self) -> str:
        return f"<Grade {self.id}>"
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)


def check_if_registered(course_code):
    course = Registeredcourses.query.filter_by(course_code=course_code).filter_by(stud_id=get_jwt_identity()).first()
    if course:
        return True
    else:
        return False