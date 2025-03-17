from app import app  # Импортируем app из app.py, а не из models.py
from models import db, Route

with app.app_context():
    routes = Route.query.all()
    for route in routes:
        if route.photo == 'img/event-01.jpg':
            route.photo = 'static/img/event-01.jpg'
            print(f"Обновлен путь для {route.name}: {route.photo}")
    db.session.commit()
    print("Путь к изображению успешно обновлен!")