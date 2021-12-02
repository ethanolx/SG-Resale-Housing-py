from .. import INPUT_BOUNDARIES
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.fields import DateField, IntegerField
from wtforms.validators import InputRequired, ValidationError, NumberRange


class PredictionForm(FlaskForm):
    floor_area = FloatField("Floor Area",
                            validators=[InputRequired(), NumberRange(min=INPUT_BOUNDARIES.loc['min', 'floor_area_sqm'], max=INPUT_BOUNDARIES.loc['max', 'floor_area_sqm'])])
    bedrooms = IntegerField("Number of Bedrooms",
                            validators=[InputRequired(), NumberRange(min=INPUT_BOUNDARIES.loc['min', 'bedrooms'], max=INPUT_BOUNDARIES.loc['max', 'bedrooms'])])
    approval_date = DateField("Approval Date",
                              validators=[InputRequired()])
    lease_commencement_year = IntegerField("Lease Commencement Year",
                                           validators=[InputRequired(), NumberRange(min=INPUT_BOUNDARIES.loc['min', 'lease_commencement_year'], max=INPUT_BOUNDARIES.loc['max', 'lease_commencement_year'])])
    submit = SubmitField("Submit for Prediction")

    def validate_approval_date(self, field):
        min_approval_date = INPUT_BOUNDARIES.loc['min', 'approval_date']
        max_approval_date = INPUT_BOUNDARIES.loc['max', 'approval_date']
        print(type(field.data))
        if type(field.data) is datetime or type(field.data) is date:
            if field.data < min_approval_date or field.data > max_approval_date:
                min_app_date_str = datetime.strftime(
                    min_approval_date, '%d/%m/%Y')
                max_app_date_str = datetime.strftime(
                    max_approval_date, '%d/%m/%Y')
                raise ValidationError(
                    f'Approval Date must be between {min_app_date_str} and {max_app_date_str}')
