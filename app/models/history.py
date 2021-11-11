#type: ignore
from .. import db
from sqlalchemy import Integer, ForeignKey, Column, Float, DateTime
from flask_login import UserMixin


class History(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('user.id'), nullable=False)
    floor_area = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    approval_date = Column(DateTime, nullable=False)
    lease_commencement_year = Column(Integer, nullable=False)
    resale_prediction = Column(Float, nullable=False)
