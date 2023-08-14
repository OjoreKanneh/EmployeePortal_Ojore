from App.models import User, Manager,Employee,Vacation
from App.database import db



def create_vacation(employee_id, start_date, end_date,vacationNum):
    new_vacation = Vacation(
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        approved=True,
        vacationNum=vacationNum
    )
    db.session.add(new_vacation)
    db.session.commit()

    # # Update the Employee's list of employees
    employee = Employee.query.get(employee_id)
    if employee:
        print(employee)
        employee.vacationDays.append(new_vacation)
        db.session.commit()
    return new_vacation

def get_vacations_for_id(id):
    return Vacation.query.filter_by(id=id).all()


def get_vacations_for_employee_id(employee_id):
    return Vacation.query.filter_by(employee_id=employee_id).all()


def get_all_vacation_json():
    vacations=Vacation.query.all()
    if not vacations:
        return[]
    vacations=[vacation.get_json() for vacation in vacations]
    return vacations