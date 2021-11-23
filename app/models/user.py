#type: ignore
from .history import History
from .. import db
from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(40), unique=True, nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
    dependency = relationship(History, cascade='all,delete,delete-orphan', passive_deletes=True)
