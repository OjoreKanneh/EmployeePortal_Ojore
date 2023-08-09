from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify

from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from App.models import db
# from App.controllers import create_user 
from App.controllers import create_manager

index_views = Blueprint('index_views', __name__, template_folder='../templates')


@index_views.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        job_title = request.form.get('job_title')
        contact = request.form.get('contact')
        # manager_check = True if request.form.get('manager_check') else False
        address = request.form.get('address')

        newManager=create_manager(username, password, job_title, contact, address)
        flash('Manager account created successfully!', 'success')
        return redirect('/login')
    return render_template('signup.html')

@index_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect('/index')
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html')









@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})