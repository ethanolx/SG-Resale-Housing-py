from flask import Blueprint, request, redirect
from flask_login import login_user
# from . import db

auth = Blueprint('auth', __name__)

@auth.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username != 'ethan' or password != '123':
        pass
    else:
        # login_user(user, remember=True)
        return redirect('/login')

@auth.route('/api/sign-up', methods=['POST'])
def signup():
    return 'Signup'

@auth.route('/logout')
def logout():
    return 'Logout'