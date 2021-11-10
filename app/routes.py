from flask import Flask, render_template, request, flash, Blueprint
from flask.helpers import make_response, url_for
from flask.wrappers import Request
from flask_login.utils import login_required, current_user
from werkzeug.utils import redirect
from .models.user import User
from .models.history import History
from .forms import LoginForm, PredictionForm, SignUpForm

routes = Blueprint("routes", __name__)

TITLE = 'RHAI'


@routes.route('/')
@routes.route('/*')
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
    past_predictions = get_past_predictions(userid=current_user.id)
    return render_template('home.html', title=TITLE, target='home', show='history', past_predictions=past_predictions)

@routes.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title=TITLE, target='login', form=form, loginMode=True)

@routes.route('/sign-up')
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        return redirect(url_for('routes.home'))
    return render_template('sign-up.html', title=TITLE, target='login', form=form, loginMode=False)


def get_past_predictions(userid):
    return History.query.filter_by(userid=userid)