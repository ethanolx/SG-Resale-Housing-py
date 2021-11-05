from flask import Flask, render_template, request, flash
from flask.helpers import make_response, url_for
from flask.wrappers import Request
from werkzeug.utils import redirect
from forms import LoginForm, SignUpForm

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

TITLE = 'RHAI'
logged_in = False

@app.route('/')
@app.route('/about')
@app.route('/index')
def index():
    return render_template('about.html', title=TITLE, target='about', logged=logged_in)

@app.route('/home')
def home():
    if logged_in:
        return render_template('home.html', title=TITLE, target='home', logged=logged_in)
    else:
        return redirect('/')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title=TITLE, target='login', form=form, loginMode=True, logged=logged_in)

@app.route('/logout')
def logout():
    global logged_in
    logged_in = False
    return render_template('about.html', title=TITLE, logged=logged_in)

@app.route('/login-user', methods=['POST'])
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'ethan' and password == '123':
        global logged_in
        logged_in = True
        return redirect('/home')
    else:
        return redirect('/login')

@app.route('/sign-up')
def sign_up():
    form = SignUpForm()
    return render_template('sign-up.html', title=TITLE, target='login', form=form, loginMode=True, logged=logged_in)

@app.route('/sign-up-user', methods=['POST'])
def sign_up_user():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            sepal_w = form.new_username.data
            petal_l = form.new_password.data
            petal_w = form.confirm_password.data
            flash(f"Prediction: ","success")
        else:
            flash("Error, cannot proceed with prediction","danger")
    return render_template('sign-up.html', title=TITLE, target='login', form=form, logged=logged_in)

# @app.route('/predict', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run()