
from werkzeug.security import generate_password_hash, check_password_hash
from App.database import db
from flask_login import UserMixin


class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    manager_id=db.Column(db.Integer, db.ForeignKey('managers.id'))
    # manager = db.relationship('Manager', backref='manager_employees')
    jobTitle=db.Column(db.String(100),unique=False, nullable=False)
    contact=db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    managerCheck = db.Column(db.Boolean, default=True, nullable=False)  # 'employee' or 'manager'
    address=db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    vacationDays= db.relationship('Vacation', backref='user', lazy=True)
    
    def __init__(self, manager_id,username, password, jobTitle, contact, managerCheck, address,email):
        self.username = username
        self.manager_id=manager_id
        self.jobTitle = jobTitle
        self.contact = contact
        self.password = generate_password_hash(password)  # Hash the password
        self.managerCheck = managerCheck
        self.address = address
        self.email=email

    def check_password(self, password):
                return check_password_hash(self.password_hash, password)

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'manager_id': self.manager_id,
            'jobTitle': self.jobTitle,
            'contact': self.contact,
            'managerCheck': self.managerCheck,
            'address': self.address,
            'email': self.email,
            'vacationDays': [vacationDays.toJSON() for vacationDay in self.vacationDays]
            # You can add other attributes as needed
        }