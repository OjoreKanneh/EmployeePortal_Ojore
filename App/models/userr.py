
from werkzeug.security import generate_password_hash, check_password_hash
from App.database import db
from flask_login import UserMixin


class Manager(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    jobTitle=db.Column(db.String(100),unique=False, nullable=False)
    contact=db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    managerCheck = db.Column(db.Boolean, default=True, nullable=False)  # 'employee' or 'manager'
    address=db.Column(db.String(100), unique=False, nullable=False)
    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)






