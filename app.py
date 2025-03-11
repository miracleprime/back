# app.py
from flask import Flask, session
import os
from routes import routes_bp
from models import db, User
from config import Config
from flask_migrate import Migrate

app = Flask(__name__, static_folder='D:\\reserv\\frond\\static', template_folder='D:\\reserv\\frond') #  Убедись, что это ПРАВИЛЬНЫЙ путь!
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(routes_bp)

app.secret_key = app.config['SECRET_KEY']  # Инициализируем сессии с секретным ключом

if __name__ == '__main__':
    app.run(debug=True)