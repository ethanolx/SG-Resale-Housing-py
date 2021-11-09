from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField, PasswordField
from wtforms.fields import DateField, IntegerField
from wtforms.validators import Email, InputRequired, Length, NumberRange, Regexp


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[InputRequired()])
    password = PasswordField(label="Password", validators=[InputRequired()])
    submit = SubmitField(label="Login")


class SignUpForm(FlaskForm):
    email = StringField(label='Your Email', validators=[
                        InputRequired(), Email()])
    new_username = StringField(
        label='New Username', validators=[InputRequired()])
    new_password = PasswordField(label='New Password', validators=[
        InputRequired(),
        Regexp(regex='[A-Z]+', message='Must contain at least one upper\n'),
        Regexp(regex='[a-z]+'),
        Regexp(regex='[0-9]+'),
        Regexp(regex='[!]+'),
        Length(min=8)
    ])
    confirm_password = PasswordField(label='Confirm Password', validators=[InputRequired(
    ), Regexp(regex='[A-Z]+'), Regexp(regex='[a-z]+'), Regexp(regex='[0-9]+'), Length(min=8), Regexp(regex='[!]+')])


class PredictionForm(FlaskForm):
    floor_area = FloatField("Floor Area",
                            validators=[InputRequired(), NumberRange(0)])
    bedrooms = IntegerField("Number of Bedrooms",
                          validators=[InputRequired(), NumberRange(1)])
    approval_date = DateField("Approval Date",
                          validators=[InputRequired()])
    lease_commencement_year = IntegerField("Lease Commencement Year",
                          validators=[InputRequired(), NumberRange(1970)])
    submit = SubmitField("Submit Prediction")
