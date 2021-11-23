from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField, PasswordField
from wtforms.fields import DateField, IntegerField
from wtforms.validators import Email, EqualTo, InputRequired, Length, NumberRange, Regexp


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[InputRequired()])
    password = PasswordField(label="Password", validators=[InputRequired()])
    submit = SubmitField(label="Login")


class SignUpForm(FlaskForm):
    email = StringField(label='Your Email', validators=[
                        InputRequired(), Email(message='Invalid email!')])
    new_username = StringField(
        label='New Username', validators=[InputRequired()])
    new_password = PasswordField(label='New Password', validators=[
        InputRequired(),
        Regexp(
            regex='.*[A-Z]+.*', message='Password must contain at least one uppercase letter!'),
        Regexp(
            regex='.*[a-z]+.*', message='Password must contain at least one lowercase letter!'),
        Regexp(regex='.*[0-9]+.*',
               message='Password must contain at least one number!'),
        Regexp(regex='.*[!@#$%^&*]+.*',
               message='Password must contain at least one special character [!@#$%^&*]!'),
        Length(min=8, message='Password must contain at least 8 characters!')
    ])
    confirm_password = PasswordField(label='Confirm Password', validators=[
        InputRequired(),
        EqualTo(fieldname='new_password', message='Passwords must match!')
    ])


class PredictionForm(FlaskForm):
    floor_area = FloatField("Floor Area",
                            validators=[InputRequired(), NumberRange(0)])
    bedrooms = IntegerField("Number of Bedrooms",
                            validators=[InputRequired(), NumberRange(1, 4)])
    approval_date = DateField("Approval Date",
                              validators=[InputRequired()])
    lease_commencement_year = IntegerField("Lease Commencement Year",
                                           validators=[InputRequired(), NumberRange(1970)])
    submit = SubmitField("Submit for Prediction")
