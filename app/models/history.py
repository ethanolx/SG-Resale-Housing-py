from .. import db
from sqlalchemy import Integer, ForeignKey, Column, Float, DateTime
from sqlalchemy.orm import validates
from flask_login import UserMixin
import cloudpickle


with open('./app/static/input_boundaries.p', 'rb') as input_bounds_file:
    input_boundaries = cloudpickle.load(file=input_bounds_file)

with open('./app/static/output_boundaries.p', 'rb') as output_bounds_file:
    output_boundaries = cloudpickle.load(file=output_bounds_file)

class History(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    floor_area = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    approval_date = Column(DateTime, nullable=False)
    lease_commencement_year = Column(Integer, nullable=False)
    resale_prediction = Column(Float, nullable=False)
    predicted_on = Column(DateTime, nullable=False)

    @validates('floor_area')
    def valid_floor_area(self, key, floor_area):
        assert input_boundaries['floor_area_sqm'].min() <= floor_area <= input_boundaries['floor_area_sqm'].max()
        return floor_area

    @validates('bedrooms')
    def valid_bedrooms(self, key, bedrooms):
        assert input_boundaries['bedrooms'].min() <= bedrooms <= input_boundaries['bedrooms'].max()
        return bedrooms

    @validates('approval_date')
    def valid_approval_date(self, key, approval_date):
        assert input_boundaries['approval_date'].min() <= approval_date <= input_boundaries['approval_date'].max()
        return approval_date

    @validates('lease_commencement_year')
    def valid_lease_commencement_year(self, key, lease_commencement_year):
        assert input_boundaries['lease_commencement_year'].min() <= lease_commencement_year <= input_boundaries['lease_commencement_year'].max()
        return lease_commencement_year

    @validates('resale_prediction')
    def valid_resale_prediction(self, key, resale_prediction):
        assert output_boundaries['min'] <= resale_prediction <= output_boundaries['max']
        return resale_prediction