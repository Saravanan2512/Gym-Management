# app/models/package.py
from app import db

class Package(db.Model):
    __tablename__ = 'packages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Float, nullable=False)
    plan_duration = db.Column(db.String(50))  # e.g., "3 months", "6 months", etc.

    # Relationship with Client
    clients = db.relationship("Client", back_populates="package")

    def __repr__(self):
        return f"<Package {self.name}>"
