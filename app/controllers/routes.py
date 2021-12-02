from flask import Flask, render_template, request, flash, Blueprint
from flask.helpers import make_response, url_for
from flask.wrappers import Request
from flask_login.utils import login_required, current_user
from .api import get_all_predictions
from ..forms.login_form import LoginForm
from ..forms.prediction_form import PredictionForm
from ..forms.sign_up_form import SignUpForm
from .api import *
from .. import TITLE

# Instantiate controller
routes = Blueprint("routes", __name__)

# Index page
@routes.route('/')
@routes.route('/about')
@routes.route('/index')
def index():
    return render_template('about.html', title=TITLE, target='about')


@routes.route('/home')
@login_required
def home():
    form = PredictionForm()
    return render_template('home.html', title=TITLE, target='home', show='new', form=form)


@routes.route('/history')
@login_required
def history():
    past_predictions = get_all_predictions(
        userid=current_user.id)  # type: ignore
    return render_template('home.html', title=TITLE, target='home', show='history', past_predictions=past_predictions, user_id=current_user.id) # type: ignore


@routes.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title=TITLE, target='login', form=form, loginMode=True)


@routes.route('/sign-up')
def sign_up():
    form = SignUpForm()
    return render_template('sign-up.html', title=TITLE, target='login', form=form, loginMode=False)
