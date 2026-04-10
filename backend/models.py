from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "role": self.role,
            "email": self.email
        }


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    organizer = db.Column(db.String(120), nullable=False)
    organizer_email = db.Column(db.String(120), nullable=True)
    participants = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "location": self.location,
            "date": self.date,
            "time": self.time,
            "description": self.description,
            "organizer": self.organizer,
            "organizer_email": self.organizer_email,
            "participants": self.participants,
            "featured": self.featured
        }