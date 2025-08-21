from app import db

class Trainer(db.Model):
    __tablename__ = 'trainers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer)
    qualities = db.Column(db.Text)
    batch = db.Column(db.String(20))  # e.g., 'Morning', 'Evening'
    photo = db.Column(db.String(100))

    # Relationship: A trainer can have many clients
    clients = db.relationship('Client', back_populates='trainer', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Trainer {self.name}>"
