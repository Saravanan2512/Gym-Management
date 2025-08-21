# app/models/client.py
from app import db
from datetime import datetime

class Client(db.Model):
    __tablename__ = 'clients'

    # ---------- Basic Info ----------
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    contact = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)

    # ---------- Status & Dates ----------
    status = db.Column(db.String(10), default='Active')  # Active / Inactive
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    billing_date = db.Column(db.Date)
    duration = db.Column(db.String(20))  # e.g., '3 months', '6 months'

    # ---------- Payment Info ----------
    payment_method = db.Column(db.String(50))
    # amount_paid = db.Column(db.Float)
    # payment_date = db.Column(db.Date)
    # payments = db.relationship("Payment", back_populates="client", cascade="all, delete-orphan")


    # ---------- Foreign Keys ----------
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'))

    # ---------- Relationships ----------
    package = db.relationship("Package", back_populates="clients")
    trainer = db.relationship("Trainer", back_populates="clients")

    # ---------- Timestamps ----------
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---------- Methods ----------
    def __repr__(self):
        return f"<Client {self.first_name} {self.last_name}>"

    def check_and_update_status(self):
        """Automatically mark client as Inactive if end date is past today."""
        if self.end_date and datetime.utcnow().date() > self.end_date:
            self.status = "Inactive"
        else:
            self.status = "Active"
