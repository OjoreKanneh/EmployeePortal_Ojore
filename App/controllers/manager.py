from App.models import User, Manager,Employee
from App.database import db

# from App.models import Manager
# from App.models import Employee


def create_manager(username, password,jobTitle,contact,address):
    newManager = Manager(username=username, password=password, jobTitle=jobTitle,
    contact=contact,managerCheck=True, address=address)
    db.session.add(newManager)
    db.session.commit()
    return newManager

def get_manager_by_username(username):
    return Manager.query.filter_by(username=username).first()

def get_manager(id):
    return manager.query.get(id)
    # sdfdjfsdj

def get_all_managers():
    return Manager.query.all()

# def get_all_users_json():
#     users = User.query.all()
#     if not users:
#         return []
#     users = [user.get_json() for user in users]
#     return users

def get_all_managers_json():
    managers=Manager.query.all()
    if not managers:
        return[]
    managers=[manager.get_json() for manager in managers]
    return managers

def get_manager_by_username_json(username):
    manager = Manager.query.filter_by(username=username).first()
    
    if manager:
        return manager.get_json()  # Assuming you have a 'get_json' method in your Manager model
    else:
        return {} 