from app import create_app
from app.extention import db

# Create the Flask app using the factory
app = create_app()

# Use app context to create tables
with app.app_context():
    db.create_all()
    print("✅ All tables created successfully.")
