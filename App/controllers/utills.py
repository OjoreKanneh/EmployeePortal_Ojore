from App.models import User, Manager,Employee
from App.database import db

def get_manager_dict(name):
    manager = Manager.query.filter_by(username=name).first()
    managerr = {
        'id': manager.id,
        'username': manager.username,
        'jobTitle': manager.jobTitle,
        'contact': manager.contact,
        'address': manager.address,
        'employees': manager.employees,
        'firstName': manager.firstName,
        'lastName': manager.lastName,
        'email':manager.email
        # 'vactaionDaysNum':manager.vactaionDaysNum
    }
    return managerr


def get_employee_dict(name):
    employee = Employee.query.filter_by(username=name).first()
    employee = {
        'id': employee.id,
        'username': employee.username,
        'jobTitle': employee.jobTitle,
        'contact': employee.contact,
        'address': employee.address,
        'email': employee.email,
        'vactaionDaysNum': employee.vactaionDaysNum,
        'vacationDays': employee.vacationDays,
        'vacationRequest':employee.vacationRequest
    }
    return employee