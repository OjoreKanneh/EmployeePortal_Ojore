from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash,session
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField,SubmitField
# from wtforms.validators import InputRequired, length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash



from flask_login import LoginManager, UserMixin, login_user, login_required, current_user,logout_user
from App.models import db,Manager
from App.controllers import create_user, create_manager
from App.controllers import get_all_managers_json,get_manager_by_username_json


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


# @index_views.route('/managerDashboard', methods=['GET'])
# def managerDash():
#     user = session.get('username')  # Retrieve user info from the session

#     print("user is ", user)
#     manager = Manager.query.filter_by(username=user).first()
#     # print(manager)
#     if manager and manager.managerCheck==True:
#         managerr=[]
#         all_managers = Manager.query.all()
        
#         for m in all_managers:
#             manager_dict = {
#                 'id': m.id,
#                 'username': m.username,
#                 'jobTitle': m.jobTitle,
#                 'contact': m.contact,
#                 'address':m.address,
#                 'employees': m.employees
#             }
#             managerr.append(manager_dict)

#         print (managerr)
#         # print (manager)
#         return render_template('managerDashboard.html', managerr=managerr)
#     else:
#         flash('You are not authorized to access this page, please login again.', 'danger')
#         return redirect('/login')
#     #  return render_template('managerdashboard.html', managers=managers)

@index_views.route('/managerDashboard', methods=['GET'])
def managerDash():
    user = session.get('username')  # Retrieve user info from the session

    print("user is ", user)
    manager = Manager.query.filter_by(username=user).first()
    # print(manager)
    if manager and manager.managerCheck==True:
        managerr = {
            'id': manager.id,
            'username': manager.username,
            'jobTitle': manager.jobTitle,
            'contact': manager.contact,
            'address': manager.address,
            'employees': manager.employees,
            'firstName': manager.firstName,
            'lastName': manager.lastName
        }
        print (managerr)
        # print (manager)
        return render_template('managerDashboard.html', managerr=managerr)
    else:
        flash('You are not authorized to access this page, please login again.', 'danger')
        return redirect('/login')



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
