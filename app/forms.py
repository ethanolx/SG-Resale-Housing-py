from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField, PasswordField
from wtforms.validators import Email, InputRequired, NumberRange, Regexp

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[InputRequired()])
    password = PasswordField(label="Password", validators=[InputRequired()])
    submit = SubmitField(label="Login")

class SignUpForm(FlaskForm):
    email = StringField(label='Your Email', validators=[InputRequired(), Email()])
    new_username = StringField(label='New Username', validators=[InputRequired()])
    new_password = PasswordField(label='New Password', validators=[InputRequired(), Regexp(regex='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')])
    confirm_password = PasswordField(label='Confirm Password', validators=[InputRequired(), Regexp(regex='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')])
    # submit = SubmitField(label='Sign Up')

class PredictionForm(FlaskForm):
    sepal_l = FloatField("Sepal Length",
                         validators=[InputRequired(), NumberRange(0, 10)])
    sepal_w = FloatField("Sepal Width",
                         validators=[InputRequired(), NumberRange(0, 10)])
    petal_l = FloatField("Petal Length",
                         validators=[InputRequired(), NumberRange(0, 10)])
    petal_w = FloatField("Petal Width",
                         validators=[InputRequired(), NumberRange(0, 10)])
    submit = SubmitField("Predict")
