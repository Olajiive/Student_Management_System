from ..utils import db
from functools import wraps
from flask_restx import abort
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from ..code_gen import code_generator

from datetime import datetime

class Admin(db.Model):
    __tablename__ = "admin"
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(80), nullable=False)
    admin_id=db.Column(db.String(70), unique=True, nullable=False, 
                       default=code_generator(f"ADM|001|{datetime.now().year}|"))
    email=db.Column(db.String(150), unique=True, nullable=False)
    password_hash=db.Column(db.Text(), nullable=False)

    def __repr__(self) -> str:
        return f"<Admin {self.id}>"
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user=get_jwt_identity()
        if not user.startswith("ADM"):
            abort(HTTPStatus.UNAUTHORIZED, message="Restricted to Admin")
        return func(*args, **kwargs)
    return wrapper 
    