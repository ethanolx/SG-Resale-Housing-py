import json
from typing import cast
from flask import Blueprint, request, redirect, flash, url_for
from flask.templating import render_template
from flask.wrappers import Request
from flask_login import login_user
from flask_login.utils import login_required, logout_user
import sqlalchemy
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from app.api import get_user
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
    form = SignUpForm(request.form)
    if form.validate():
        try:
            email = request.form.get('email')
            new_username = request.form.get('new_username')
            new_password = request.form.get('new_password')
            data = json.dumps({
                'email': email,
                'username': new_username,
                'password': new_password
            })
            del new_password
            response = requests.post(
                url=request.host_url + 'api/user/add', json=data)
            print(response.json()['new_user_id'])
            new_user = get_user(response.json()['new_user_id'])
            login_user(user=new_user)
            return redirect(url_for('routes.home'))
        except sqlalchemy.exc.IntegrityError as err:
            import re
            duplicate = re.match('.*user\\.(\\w+)', str(err)
                                 ).group(1)  # type: ignore
            flash(duplicate.capitalize() + ' already taken!')
            return redirect(url_for('routes.sign_up'))
    else:
        return render_template('sign-up.html', title='RHAI', target='login', form=form, loginMode=False)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))
