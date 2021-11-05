from flask import Flask, render_template, request, flash
from forms import LoginForm, SignUpForm

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

TITLE = 'RHAI'

def default_template(page='index.html', title=TITLE, logged=False, **kwargs):
    return render_template(page, title=title, logged=logged, **kwargs)

@app.route('/')
@app.route('/about')
@app.route('/index')
def home():
    return default_template(page='about.html')

@app.route('/login')
def login():
    form1 = LoginForm()
    form2 = SignUpForm()
    return default_template(page='login.html', form1=form1, form2=form2, loginMode=False)

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