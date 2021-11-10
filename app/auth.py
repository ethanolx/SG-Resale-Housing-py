from typing import cast
from flask import Blueprint, request, redirect, flash, url_for
from flask_login import login_user
from flask_login.utils import logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.forms import SignUpForm
from app.routes import sign_up
from . import db
from .models.user import User

auth = Blueprint('auth', __name__)


@auth.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not password or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect('/login')

    login_user(user=user, remember=True)
    return redirect('/home')


@auth.route('/api/sign-up', methods=['POST'])
def sign_up():
    email = request.form.get('email')
    new_username = request.form.get('new_username')
    new_password = cast(str, request.form.get('new_password'))
    confirm_password = request.form.get('confirm_password')
    if SignUpForm(request.form).validate_on_submit():
        new_user = User(email=email, username=new_username,
                        password=generate_password_hash(new_password, method='sha256'))
        del new_password
        del confirm_password
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('routes.home'))
    else:
        return redirect(url_for('routes.sign_up'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))
