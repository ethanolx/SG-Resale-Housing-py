from .. import INPUT_BOUNDARIES
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.fields import DateField, IntegerField
from wtforms.validators import InputRequired, ValidationError

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

    def validate_floor_area(self, field):
        min_floor_area = INPUT_BOUNDARIES.loc['min', 'floor_area_sqm']
        max_floor_area = INPUT_BOUNDARIES.loc['max', 'floor_area_sqm']

        if field.data < min_floor_area or field.data > max_floor_area:
            raise ValidationError(
                f'Floor Area must be between {min_floor_area} and {max_floor_area}')

    def validate_bedrooms(self, field):
        min_bedrooms = INPUT_BOUNDARIES.loc['min', 'bedrooms']
        max_bedrooms = INPUT_BOUNDARIES.loc['max', 'bedrooms']

        if field.data < min_bedrooms or field.data > max_bedrooms:
            raise ValidationError(
                f'Bedrooms must be between {min_bedrooms} and {max_bedrooms}')

    def validate_approval_date(self, field):
        min_approval_date = INPUT_BOUNDARIES.loc['min', 'approval_date']
        max_approval_date = INPUT_BOUNDARIES.loc['max', 'approval_date']

        if field.data < min_approval_date or field.data > max_approval_date:
            min_app_date_str = datetime.strftime(min_approval_date, '%d/%m/%Y')
            max_app_date_str = datetime.strftime(max_approval_date, '%d/%m/%Y')
            raise ValidationError(
                f'Approval Date must be between {min_app_date_str} and {max_app_date_str}')

    def validate_lease_commencement_year(self, field):
        min_lcy = INPUT_BOUNDARIES.loc['min', 'lease_commencement_year']
        max_lcy = INPUT_BOUNDARIES.loc['max', 'lease_commencement_year']

        if field.data < min_lcy or field.data > max_lcy:
            raise ValidationError(
                f'Lease Commencement Year must be between {min_lcy} and {max_lcy}')