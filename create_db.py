
# create_db.py
from models import app, db

with app.app_context():
    pass
    db.create_all(),

print("Таблицы базы данных (при необходимости) успешно созданы!")