from flask_app.extensions import db

class SiteConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_title = db.Column(db.String(100), nullable=False, default="My Site")
    logo_path = db.Column(db.String(255), nullable=True)  # Path to uploaded logo
    favicon_path = db.Column(db.String(255), nullable=True)  # Path to uploaded favicon
    primary_color = db.Column(db.String(7), nullable=False, default="#ff3860")  # Hex color
    secondary_color = db.Column(db.String(7), nullable=False, default="#3273dc")  # Hex color
    tertiary_color = db.Column(db.String(7), nullable=False, default="#23d160")  # Hex color
    heading_font = db.Column(db.String(100), nullable=False, default="Arial")
    subheading_font = db.Column(db.String(100), nullable=False, default="Verdana")
    paragraph_font = db.Column(db.String(100), nullable=False, default="Georgia")
    maintenance_mode = db.Column(db.Boolean, default=False)  # Toggle maintenance mode
    maintenance_message = db.Column(db.Text, nullable=True)  # Custom maintenance message
    meta_description = db.Column(db.String(255), nullable=True)  # For SEO
    analytics_code = db.Column(db.Text, nullable=True)  # Custom analytics code

    def __repr__(self):
        return f"<SiteConfig {self.site_title}>"
