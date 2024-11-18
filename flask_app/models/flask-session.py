from flask_session import SqlAlchemySessionInterface
from flask_app.extensions import db

class FlaskSession(SqlAlchemySessionInterface):
    pass
