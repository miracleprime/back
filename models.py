from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)
app.config.from_object('config.Config')

# Ensure the instance folder exists:
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db = SQLAlchemy(app)

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    activity_type = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
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