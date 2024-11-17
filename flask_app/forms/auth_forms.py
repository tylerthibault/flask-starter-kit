from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class LoginForm(FlaskForm):
    # Email field with email validation
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Enter a valid email address."),
        ],
    )
    
    # Password field with length validation
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters long."),
        ],
    )
    
    # Remember me checkbox
    remember_me = BooleanField("Remember Me")
    
    # Submit button
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    # Username field with a regex validator for alphanumeric characters
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=25, message="Username must be between 3 and 25 characters."),
            Regexp(
                "^[a-zA-Z0-9_]+$",
                message="Username must contain only letters, numbers, or underscores."
            )
        ],
    )
    
    # Email field with email validation
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Enter a valid email address.")
        ],
    )
    
    # Password field with length validation
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=50, message="Password must be at least 6 characters long."),
        ],
    )
    
    # Password confirmation field with matching validation
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match.")
        ],
    )
    
    # Terms and conditions checkbox
    accept_terms = BooleanField(
        "I accept the Terms and Conditions",
        validators=[DataRequired(message="You must accept the terms and conditions.")],
    )
    
    # Submit button
    submit = SubmitField("Register")