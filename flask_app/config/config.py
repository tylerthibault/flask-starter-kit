import os
from math import ceil

from flask import app
from requests import Session

from flask_app.extensions import db

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
    last = 0
    for num in range(1, self.pages + 1):
        if (
            num <= left_edge
            or (num > self.page - left_current - 1 and num < self.page + right_current)
            or num > self.pages - right_edge
        ):
            if last + 1 != num:
                yield None
            yield num
            last = num
