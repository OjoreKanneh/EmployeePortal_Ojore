import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from datetime import date

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import( create_user, get_all_users_json, get_all_users )
from App.controllers import create_manager, get_all_managers, get_all_managers_json,create_employee, get_all_employees_json, create_vacation,get_all_vacation_json
# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    start_date = date(2023, 8, 15)  # Replace with the desired start date
    end_date = date(2023, 8, 20)
    create_manager('bob', 'bobpass','supervisor','2732761','street','Bob','Smith','bob@tis.com')
    create_employee('ojoree',1,'intern','277900','ojore','street','ojoree@tis.com',20,True)
    create_employee('rob',1,'programmer','277950','robpass','street','rob@tis.com',20,False)
    create_vacation(1,start_date,end_date,20)
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('manager', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_manager_command(format):
    if format == 'string':
        print(get_all_managers_json())
    # else:
    #     print(get_all_managers_json())

app.cli.add_command(user_cli) # add the group to the cli




user_cli = AppGroup('employee', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("manager_id", default=1)
# @click.argument("jobTitle", default="programmer")
# @click.argument("contact", default=1234949)
# @click.argument("password", default="robpass")
# @click.argument("address", default="road")
# @click.argument("email", default="rob@tis.com")



# def create_user_command(username, manager_id,jobTitle,contact,password,address,email):
#     create_user(username, manager_id,jobTitle,contact,password,address,email)
#     print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_manager_command(format):
    if format == 'string':
        print(get_all_employees_json())
    # else:
    #     print(get_all_managers_json())

app.cli.add_command(user_cli) # add the group to the cli


user_cli = AppGroup('vacation', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("manager_id", default=1)
# @click.argument("jobTitle", default="programmer")
# @click.argument("contact", default=1234949)
# @click.argument("password", default="robpass")
# @click.argument("address", default="road")
# @click.argument("email", default="rob@tis.com")



# def create_user_command(username, manager_id,jobTitle,contact,password,address,email):
#     create_user(username, manager_id,jobTitle,contact,password,address,email)
#     print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_manager_command(format):
    if format == 'string':
        print(get_all_vacation_json())
    # else:
    #     print(get_all_managers_json())

app.cli.add_command(user_cli) # add the group to the cli





'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
