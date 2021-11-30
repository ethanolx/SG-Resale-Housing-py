from datetime import datetime
from .. import INPUT_BOUNDARIES, db, INPUT_BOUNDARIES, OUTPUT_BOUNDARIES
from sqlalchemy import Integer, ForeignKey, Column, Float, DateTime
from sqlalchemy.orm import validates


class History(db.Model):  # type:ignore
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    floor_area = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    approval_date = Column(DateTime, nullable=False)
    lease_commencement_year = Column(Integer, nullable=False)
    resale_prediction = Column(Float, nullable=False)
    predicted_on = Column(DateTime, nullable=False)

    @validates('userid')
    def valid_user_id(self, key, userid):
        assert type(userid) is int, 'User id in wrong format'
        assert userid is not None, 'Null user id'
        return userid

    @validates('floor_area')
    def valid_floor_area(self, key, floor_area):
        assert type(floor_area) is float, 'Floor area in wrong format'
        assert INPUT_BOUNDARIES.loc['min',
                                    'floor_area_sqm'] <= floor_area <= INPUT_BOUNDARIES.loc['max', 'floor_area_sqm'], 'Floor area out of range'
        return floor_area

    @validates('bedrooms')
    def valid_bedrooms(self, key, bedrooms):
        assert type(bedrooms) is int, 'Bedrooms in wrong format'
        assert INPUT_BOUNDARIES.loc['min',
                                    'bedrooms'] <= bedrooms <= INPUT_BOUNDARIES.loc['max', 'bedrooms'], 'Bedrooms out of range'
        return bedrooms

    @validates('approval_date')
    def valid_approval_date(self, key, approval_date):
        assert type(approval_date) is datetime, 'Approval date in wrong format'
        assert INPUT_BOUNDARIES.loc['min',
                                    'approval_date'] <= approval_date <= INPUT_BOUNDARIES.loc['max', 'approval_date'], 'Approval date out of range'
        return approval_date

    @validates('lease_commencement_year')
    def valid_lease_commencement_year(self, key, lease_commencement_year):
        assert type(lease_commencement_year) is int, 'Lease commencement year in wrong format'
        assert INPUT_BOUNDARIES.loc['min',
                                    'lease_commencement_year'] <= lease_commencement_year <= INPUT_BOUNDARIES.loc['max', 'lease_commencement_year'], 'Lease commencement year out of range'
        return lease_commencement_year

    @validates('resale_prediction')
    def valid_resale_prediction(self, key, resale_prediction):
        assert type(resale_prediction) is float, 'Resale price prediction in wrong format'
        assert OUTPUT_BOUNDARIES['min'] <= resale_prediction <= OUTPUT_BOUNDARIES['max'], 'Resale price prediction out of range'
        return resale_prediction
