from flask_app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == "__main__":
    # Run the Flask development server
    app.run(host="0.0.0.0", port=5000, debug=True)
