from App.models import User, Manager,Employee
from App.database import db

# def create_employee(manager, username, password, jobTitle, contact, address):
#     new_employee = Employee(username=username, password=password, jobTitle=jobTitle,
#                             contact=contact, address=address, manager=manager)
#     db.session.add(new_employee)
#     db.session.commit()
#     return new_employee


def create_employee(username, manager_id, jobTitle,contact,password,address, email):
    new_employee = Employee(
        username=username,
        manager_id=manager_id,
        jobTitle=jobTitle,
        contact=contact,
        password=password,
        managerCheck=False,
        address=address,
        email=email
    )

    db.session.add(new_employee)
    db.session.commit()

    # Update the manager's list of employees
    manager = Manager.query.get(manager_id)
    if manager:
        print(manager)
        manager.employees.append(new_employee)
        db.session.commit()
    return new_employee

def get_all_employees_json():
    employees=Employee.query.all()
    if not employees:
        return[]
    employees=[employee.get_json() for employee in employees]
    return employees