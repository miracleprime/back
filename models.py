# models.py
from flask_sqlalchemy import SQLAlchemy
from pip._internal.utils import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import datetime  # Ensure the standard datetime is imported
from datetime import datetime

db = SQLAlchemy()

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    activity_type = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    calories = db.Column(db.Integer, nullable=True)
    relief = db.Column(db.String(200), nullable=True)
    rest_zones = db.Column(db.Boolean, default=False)
    drinking_fountains = db.Column(db.Boolean, default=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(200), nullable=True)
    approved = db.Column(db.Boolean, default=False)  # Добавлено поле

    def __repr__(self):
        return f'<Route {self.name}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Оценка от 1 до 5
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    route = db.relationship('Route', backref=db.backref('review', lazy=True))
    user = db.relationship('User', backref=db.backref('review', lazy=True))

    def __repr__(self):
        return f'<Review {self.id} for Route {self.route_id}>'