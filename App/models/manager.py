
from werkzeug.security import generate_password_hash, check_password_hash
from App.database import db
from flask_login import UserMixin


class Manager(db.Model, UserMixin):
        __tablename__ = 'managers'

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100) , nullable=False)
        password = db.Column(db.String(128), nullable=False)
        jobTitle=db.Column(db.String(100), nullable=False)
        contact=db.Column(db.Integer, nullable=False)

        managerCheck = db.Column(db.Boolean, default=True, nullable=False)  # 'employee' or 'manager'
        address=db.Column(db.String(100), unique=False, nullable=False)
        employees=db.relationship('Employee', backref='manager', lazy=True)
        firstName=db.Column(db.String(100) , nullable=False)
        lastName=db.Column(db.String(100) , nullable=False)
        email = db.Column(db.String(100), unique=True, nullable=False)

    
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
        # return check_password_hash(self.password_hash, password)
        def __init__(self, username, password, jobTitle, contact, managerCheck, address,firstName,lastName,email):
                self.username = username
                self.password = generate_password_hash(password)  # Hash the password
                self.jobTitle = jobTitle
                self.contact = contact
                self.managerCheck = managerCheck
                self.address = address
                self.firstName=firstName
                self.lastName=lastName   
                self.email=email    


        def check_password(self, password):
                return check_password_hash(self.password_hash, password)


        def __repr__(self):
                return f"<Manager(id={self.id}, username={self.username}, jobTitle={self.jobTitle})>"

        def get_json(self):
                return {
                'id': self.id,
                'username': self.username,
                'jobTitle': self.jobTitle,
                'contact': self.contact,
                'managerCheck': self.managerCheck,
                'address': self.address,
                'employees': [employee.toJSON() for employee in self.employees],
                'firstName':self.firstName,
                'lastName':self.lastName,
                'email':self.email
                }
        

        # def to_json(self):
        #         json_manager = {
        #             'id': self.id,
        #             'username': self.username,
        #             'jobTitle': self.jobTitle,
        #             'contact': self.contact,
        #             'managerCheck': self.managerCheck,
        #             'address': self.address,
        #             'employees': [employee.id for employee in self.employees]
        #         }
        #         return json_manager
