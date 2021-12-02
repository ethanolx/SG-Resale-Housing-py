from flask import Blueprint, request, redirect, flash, url_for, json

from flask.templating import render_template
from flask_login import login_user
from flask_login.utils import login_required, logout_user
from werkzeug.security import check_password_hash
import requests
from .. import TITLE
from .api import get_user
from ..forms.sign_up_form import SignUpForm
from ..models.user import User

auth = Blueprint('auth', __name__)


@auth.route('/auth/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not (user and password and check_password_hash(user.password, password)):
        flash('Please check your login details and try again.', category='warning')
        return redirect(url_for('routes.login'))

    print(not (user and password and check_password_hash(user.password, password)))
    login_user(user=user, remember=True)
    return redirect(url_for('routes.home'))


@auth.route('/auth/sign-up', methods=['POST'])
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
            assert response.status_code == 200
            new_user = get_user(response.json()['new_user_id'])
            login_user(user=new_user)
            return redirect(url_for('routes.home'))
        except AssertionError:
            flash(response.json()['error'], category='error')
            return redirect(url_for('routes.sign_up'))
    else:
        return render_template('sign-up.html', title=TITLE, target='login', form=form, loginMode=False)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))
