from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField,SubmitField
# from wtforms.validators import InputRequired, length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash



from flask_login import LoginManager, UserMixin, login_user, login_required, current_user,logout_user
from App.models import db,Manager
# from App.controllers import create_user 
from App.controllers import create_manager


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
    if request.method == 'POST':
        data=request.form
        print("Received form data:", data)
        newManager=create_manager(data['username'], data['password'], data['jobTitle'], data['contact'], data['address'])
        # print(username)
        flash('Manager account created successfully!', 'success')
        return redirect('/login')
    return render_template('signup.html')

@index_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data=request.form
        print("Received form data:", data)
        user = Manager.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password,data['password']):
        #     # login_user(user)
            flash('You are logged in!', 'success')
            print("your are logged in")
            return redirect('/index')
            if user.managerCheck==True:
                return redirect('/index')
            else:
                return redirect ('/hello')
        else:
            flash('Invalid username or password. Please try again.', 'danger')

        # form=LoginForm()
    return render_template('login.html')




@index_views.route('/index', methods=['GET'])
def index_page():
    return render_template('index.html')


@index_views.route('/hello', methods=['GET'])
def hello_world():
    return "Hello, World!"



@index_views.route('/', methods=['GET'])
def home_page():
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