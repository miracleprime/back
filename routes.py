from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
from models import app, db, Route

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/routes', methods=['GET', 'POST'])
def get_routes():
    if request.method == 'GET':
        activity_type = request.args.get('activity_type')
        if activity_type:
            routes = Route.query.filter_by(activity_type=activity_type, approved=True).all()
        else:
            routes = Route.query.filter_by(approved=True).all()

        route_list = []
        for route in routes:
            route_data = {
                'id': route.id,
                'name': route.name,
                'description': route.description,
                'activity_type': route.activity_type,
                'difficulty': route.difficulty,
                'distance': route.distance,
                'duration': route.duration,
                'calories': route.calories,
                'relief': route.relief,
                'rest_zones': route.rest_zones,
                'drinking_fountains': route.drinking_fountains,
                'latitude': float(route.latitude),
                'longitude': float(route.longitude),
                'photo': route.photo,  # Добавлено поле photo - **ОШИБКА**
                'approved': route.approved
            }
             # Добавлено логирование
            route_list.append(route_data)

        return jsonify(route_list)
    elif request.method == 'POST':
        data = request.get_json()
        new_route = Route(
            name=data['name'],
            description=data['description'],
            activity_type=data['category'],
            difficulty='неизвестно',
            distance=0,
            duration=0,
            latitude=data['latitude'],
            longitude=data['longitude'],
            photo=data['photo'],
            rest_zones=False,
            drinking_fountains=False,
            calories=0,
            relief='Неизвестно',
            approved=False  # По умолчанию не одобрено
        )
        db.session.add(new_route)
        db.session.commit()
        return jsonify({'message': 'Место успешно добавлено и ожидает модерации'}), 201

    return jsonify({'message': 'Метод не разрешен'}), 405


@app.route('/api/moderate', methods=['GET', 'POST'])
def moderate_routes():
    if request.method == 'GET':
        # Получить список мест, ожидающих модерации
        pending_routes = Route.query.filter_by(approved=False).all()
        route_list = []
        for route in pending_routes:
            route_data = {
                'id': route.id,
                'name': route.name,
                'description': route.description,
                'activity_type': route.activity_type,
                'difficulty': route.difficulty,
                'distance': route.distance,
                'duration': route.duration,
                'calories': route.calories,
                'relief': route.relief,
                'rest_zones': route.rest_zones,
                'drinking_fountains': route.drinking_fountains,
                'latitude': float(route.latitude),
                'longitude': float(route.longitude),
                 'photo': route.photo,  # Добавлено поле photo **ИСПРАВЛЕННО**
                'approved': route.approved
            }
            route_list.append(route_data)
        return jsonify(route_list)
    elif request.method == 'POST':
        data = request.get_json()
        route_id = data['id']
        action = data['action']  # 'approve' или 'reject'

        route = Route.query.get(route_id)
        if route:
            if action == 'approve':
                route.approved = True
            elif action == 'reject':
                db.session.delete(route)
            db.session.commit()
            return jsonify({'message': 'Действие выполнено'}), 200
        else:
            return jsonify({'message': 'Место не найдено'}), 404
    return jsonify({'message': 'Метод не разрешен'}), 405