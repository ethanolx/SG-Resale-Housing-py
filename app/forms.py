from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField, PasswordField
from wtforms.fields import DateField, IntegerField
from wtforms.validators import Email, EqualTo, InputRequired, Length, NumberRange, Regexp, ValidationError
from . import input_boundaries


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
                            validators=[InputRequired()])
    bedrooms = IntegerField("Number of Bedrooms",
                            validators=[InputRequired()])
    approval_date = DateField("Approval Date",
                              validators=[InputRequired()])
    lease_commencement_year = IntegerField("Lease Commencement Year",
                                           validators=[InputRequired()])
    submit = SubmitField("Submit for Prediction")

    def validate_floor_area(form, field):
        min_fa = input_boundaries.loc['min', 'floor_area_sqm']
        max_fa = input_boundaries.loc['max', 'floor_area_sqm']

        if field.data < min_fa or field.data > max_fa:
            raise ValidationError(
                f'Floor Area must be between {min_fa} and {max_fa}')

    def validate_bedrooms(form, field):
        min_bedrooms = input_boundaries.loc['min', 'bedrooms']
        max_bedrooms = input_boundaries.loc['max', 'bedrooms']

        if field.data < min_bedrooms or field.data > max_bedrooms:
            raise ValidationError(
                f'Bedrooms must be between {min_bedrooms} and {max_bedrooms}')

    def validate_approval_date(form, field):
        min_approval_date = input_boundaries.loc['min', 'approval_date']
        max_approval_date = input_boundaries.loc['max', 'approval_date']

        if field.data < min_approval_date or field.data > max_approval_date:
            min_app_date_str = datetime.strftime(min_approval_date, '%Y-%m-%d')
            max_app_date_str = datetime.strftime(max_approval_date, '%Y-%m-%d')
            raise ValidationError(
                f'Approval Date must be between {min_app_date_str} and {max_app_date_str}')

    def validate_lease_commencement_year(form, field):
        min_lcy = input_boundaries.loc['min', 'lease_commencement_year']
        max_lcy = input_boundaries.loc['max', 'lease_commencement_year']

        if field.data < min_lcy or field.data > max_lcy:
            raise ValidationError(
                f'Lease Commencement Year must be between {min_lcy} and {max_lcy}')
