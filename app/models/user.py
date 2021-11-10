#type: ignore
from .. import db
from sqlalchemy import Integer, Column, String
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(40), unique=True, nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
