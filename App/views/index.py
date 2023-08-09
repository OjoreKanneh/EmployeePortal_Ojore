from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField,SubmitField
# from wtforms.validators import InputRequired, length, ValidationError



from flask_login import LoginManager, UserMixin, login_user, login_required, current_user,logout_user
from App.models import db
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
        # username = request.form.get('username')
        # password = request.form.get('password')
        # job_title = request.form.get('job_title')
        # contact = request.form.get('contact')
        # # manager_check = True if request.form.get('manager_check') else False
        # address = request.form.get('address')
        # print("Received username from form:", username)
        # print("Received password from form:", password)
        # print("Received job_title from form:", job_title)
        # print("Received contact from form:", contact)
        # print("Received address from form:", address)
        print("Received form data:", data)
        newManager=create_manager(data['username'], data['password'], data['jobTitle'], data['contact'], data['address'])
        # print(username)
        flash('Manager account created successfully!', 'success')
        return redirect('/login')
    return render_template('signup.html')

@index_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect('/index')
        else:
            flash('Invalid username or password. Please try again.', 'danger')

        # form=LoginForm()
    return render_template('login.html')




@index_views.route('/index', methods=['GET'])
def index_page():
    return render_template('index.html')




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