from flask_app import create_app
from flask_app.extensions import db
from flask_app.utils.db_population import populate_roles_and_permissions, populate_sys_admin_user

# Create the Flask application instance
app = create_app()

with app.app_context():
    db.create_all()  # Creates tables based on the models
    populate_roles_and_permissions()
    populate_sys_admin_user()

if __name__ == "__main__":
    # Run the Flask development server
    app.run(host="0.0.0.0", port=5000, debug=True)
