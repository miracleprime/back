
# create_db.py
from models import app, db

with app.app_context():
    pass #  Удаляем db.create_all(), т.к. миграции это делают

print("Таблицы базы данных (при необходимости) успешно созданы!")