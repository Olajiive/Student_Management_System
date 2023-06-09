from ..utils import db
import datetime
from sqlalchemy import CheckConstraint


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer(), primary_key=True)
    course_title = db.Column(db.String(), nullable=False)
    course_code = db.Column(db.String(), nullable=False)
    course_unit = db.Column(db.Integer(), nullable=False)
    teacher = db.Column(db.String(), nullable=False)
    registered_student = db.relationship("Registeredcourses", backref="stud", lazy=True)
    registered_courses = db.relationship("Registeredcourses", backref="course", lazy=True,
                                         overlaps="registered_student, stud", viewonly=True)

    def __repr__(self) -> str:
        return f"<Course {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
