from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Optional
from wtforms.fields.core import Field
from wtforms.widgets import Input

class ColorInput(Input):
    input_type = "color"

class ColorField(StringField):
    widget = ColorInput()

class SiteConfigForm(FlaskForm):
    site_title = StringField("Site Title", validators=[DataRequired()])
    logo = FileField("Site Logo", validators=[Optional()])
    favicon = FileField("Favicon", validators=[Optional()])
    primary_color = ColorField("Primary Color", validators=[DataRequired()])
    secondary_color = ColorField("Secondary Color", validators=[DataRequired()])
    tertiary_color = ColorField("Tertiary Color", validators=[DataRequired()])
    heading_font = StringField("Heading Font", validators=[DataRequired()])
    subheading_font = StringField("Subheading Font", validators=[DataRequired()])
    paragraph_font = StringField("Paragraph Font", validators=[DataRequired()])
    maintenance_mode = BooleanField("Enable Maintenance Mode")
    maintenance_message = TextAreaField("Maintenance Mode Message", validators=[Optional()])
    meta_description = TextAreaField("Meta Description", validators=[Optional()])
    analytics_code = TextAreaField("Analytics Code", validators=[Optional()])
    submit = SubmitField("Save Changes")
