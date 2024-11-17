from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectMultipleField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class EditUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    sys_admin = BooleanField("Admin Privileges")
    submit = SubmitField("Save Changes")

class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    roles = SelectMultipleField('Roles', coerce=int)  # Multi-select for roles
    submit = SubmitField('Add User')
