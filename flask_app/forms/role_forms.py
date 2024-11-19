from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length

class EditRoleForm(FlaskForm):
    # Role Name
    name = StringField(
        "Role Name",
        validators=[DataRequired(), Length(min=3, max=50)],
        render_kw={"class": "input", "placeholder": "Enter role name"}
    )

    # Description (Optional Field)
    description = TextAreaField(
        "Description",
        validators=[Length(max=255)],  # Optional field
        render_kw={"class": "textarea", "placeholder": "Enter role description"}
    )

    # Permissions
    permissions = SelectMultipleField(
        "Permissions",
        coerce=int,  # Expect permission IDs as integers
        render_kw={"class": "select is-multiple"}
    )

    # Submit button
    submit = SubmitField("Save Changes", render_kw={"class": "button is-primary"})

