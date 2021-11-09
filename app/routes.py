from flask import Flask, render_template, request, flash, Blueprint
from flask.helpers import make_response, url_for
from flask.wrappers import Request
from werkzeug.utils import redirect

from .forms import LoginForm, PredictionForm, SignUpForm

routes = Blueprint("routes", __name__)

TITLE = 'RHAI'
logged_in = False

@routes.route('/')
@routes.route('/about')
@routes.route('/index')
def index():
    return render_template('about.html', title=TITLE, target='about', current_user=user)

@routes.route('/home')
def home():
    if not logged_in:
        form = PredictionForm()
        user = User()
        return render_template('home.html', title=TITLE, target='home', form=form, current_user=user)
    else:
        return redirect('/')

@routes.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title=TITLE, target='login', form=form, loginMode=True)

@routes.route('/logout')
def logout():
    global logged_in
    logged_in = False
    return redirect('/about')

@routes.route('/sign-up')
def sign_up():
    form = SignUpForm()
    user = User()
    return render_template('sign-up.html', title=TITLE, target='login', form=form, loginMode=True, current_user=user)

@routes.route('/api/sign-up', methods=['POST'])
def sign_up_user():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            new_username = form.new_username.data
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data
            # flash(f"Prediction: ","success")
        else:
            flash("Error, cannot proceed with prediction","danger")
    return render_template('sign-up.html', title=TITLE, target='login', form=form)

# @routes.route('/predict', methods=['GET', 'POST'])
# def predict():
#     form = PredictionForm()
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             sepal_l = form.sepal_l.data
#             sepal_w = form.sepal_w.data
#             petal_l = form.petal_l.data
#             petal_w = form.petal_w.data
#             flash(f'Prediction: ', 'success')
#         else:
#             flash('Error, cannot proceed with prediction', 'danger')
#     return render_template('index.html', title='Enter Iris Parameters', form=form, index=True)