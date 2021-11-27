from .history import History
from .. import db
from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import validates
from flask_login import UserMixin
from email_validator import EmailNotValidError, validate_email
import re

class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(40), unique=True, nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(30), nullable=False)

    @validates('email')
    def valid_email(self, key, email: str):
        normalized_email = validate_email(email)
        return normalized_email.email

    @validates('username')
    def valid_username(self, key, username: str):
        assert username != '', 'Username cannot be empty'
        return username
