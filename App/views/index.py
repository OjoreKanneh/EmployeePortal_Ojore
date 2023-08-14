from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash,session
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField,SubmitField
# from wtforms.validators import InputRequired, length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash



from flask_login import LoginManager, UserMixin, login_user, login_required, current_user,logout_user
from App.models import db,Manager,Employee,Vacation
# from App.controllers import create_user, create_manager,create_employee,create_vacation
# from App.controllers import get_all_managers_json,get_manager_by_username_json

from App.controllers import *


index_views = Blueprint('index_views', __name__, template_folder='../templates')

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view="login"

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class LoginForm(FlaskForm):
#     username=StringField(validators=[InputRequired(),length(
#         min=4, max=20)], render_kw={"placeholder": "Username"}
#     )


#     password=PasswordField(validators=[InputRequired(),length(
#         min=4, max=20)], render_kw={"placeholder": "Password"}
#     )

#     submit=SubmitField("Login")


@index_views.route('/signup', methods=['GET', 'POST'])
def signup():
    form_data = {}
    if request.method == 'POST':
        data=request.form
        print("Received form data:", data)
        existing_manager = Manager.query.filter_by(email=data['email']).first()
        if existing_manager:
            flash('An account with this email already exists. Please use a different email.', 'danger')
            form_data=data
            return render_template('signup.html', form_data=form_data)  # Redirect back to the signup page

        newManager=create_manager(data['username'], data['password'], data['jobTitle'], data['contact'], data['address'],data['firstName'],data['lastName'],data['email'])
        # print(username)
        flash('Manager account created successfully!', 'success')
        return redirect('/login')
    return render_template('signup.html',form_data = form_data )

@index_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data=request.form
        print("Received form data:", data)
        user = Manager.query.filter_by(email=data['email']).first()

        if user and check_password_hash(user.password,data['password']):
        #     # login_user(user)
            flash('You are logged in!', 'success')
            print("your are logged in")
            # return redirect('/index')
            if user.managerCheck==True:
                session['username'] = user.username # Store user info in the session
                return redirect('/managerDashboard')
            else:
                return redirect ('/hello')
        else:
            flash('Invalid email or passwordd. Please try again.', 'danger')

        # form=LoginForm() 

    return render_template('login.html')




@index_views.route('/index', methods=['GET'])
def index_page():
    
    return render_template('index.html')
    

@index_views.route('/create_employee', methods=['POST'])
def employeeCreate():
    user = session.get('username')
    print("user iss ", user)
    form_data={}
    if request.method=='POST':
        data=request.form
        print("Received form data:", data)
        existing_employee = Employee.query.filter_by(email=data['email']).first()
        if existing_employee:
            manager = Manager.query.filter_by(username=user).first()
            if manager and manager.managerCheck==True:
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
            email_error = 'An account with this email already exists. Please use a different email.'
            flash('An account with this email already exists. Please use a different email.', 'danger')
            # form_data=data
            return render_template('managerDashboard.html',managerr=managerr)

        
        newEmployee=create_employee(data['username'],data['manager_id'],data['jobTitle'],data['contact'],data['password'],data['address'],data['email'],data['vactaionDaysNum'])
        flash('Employee account created successfully!', 'success')
        return redirect('/managerDashboard')
    # return render_template('signup.html'



@index_views.route('/managerDashboard', methods=['GET'])
def managerDash():
    user = session.get('username')  # Retrieve user info from the session

    print("user is ", user)
    manager = Manager.query.filter_by(username=user).first()
    if manager and manager.managerCheck==True:
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
        print (managerr)
        # print (manager)
        return render_template('managerDashboard.html', managerr=managerr)
    else:
        flash('You are not authorized to access this page, please login again.', 'danger')
        return redirect('/login')




@index_views.route('/vacation_info/<int:employee_id>')
def vacation_info(employee_id):
    # Assuming you have a function to fetch employee and vacation information
    employee = get_employee_by_id(employee_id)
    vacations = get_vacations_for_employee_id(employee_id)
    
    return render_template('vacation_info.html', employee=employee, vacations=vacations)

@index_views.route('/search_employee', methods=['GET'])
def search_employee():
    user = session.get('username')  # Retrieve user info from the session

    print("user is for search", user)
    email = request.args.get('email', '').strip()
    searched_employee = None
    print("email is ",email)
    
    if email:
        searched_employee = get_employee_by_email(email)  # Replace with your function to get employee by email
        print(" searched employee is ",searched_employee)
        managerr=get_manager_dict(user)
        if searched_employee is None:
            flash('No user with this email', 'danger')
            return redirect('/managerDashboard')

        return render_template('managerDashboard.html', managerr=managerr, searched_employee=searched_employee)
    # else:
    #     flash('no user with this email', 'danger')
    #     return redirect('/managerDashboard')


    
    return render_template('managerDashboard.html', managerr=managerr, searched_employee=searched_employee)

@index_views.route('/', methods=['GET'])
def home_page():
    session.clear()
    print("Session contents:", session)
    return render_template('home.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
