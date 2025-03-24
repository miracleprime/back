from flask import Flask, jsonify, request, url_for, session, render_template, redirect, Blueprint
from flask_cors import CORS
from models import db, Route, User, Review
from werkzeug.security import generate_password_hash, check_password_hash
import os

routes_bp = Blueprint('routes', __name__)
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'D:\\reserv\\frond')

CORS(routes_bp, resources={r"/*": {"origins": "*"}})

#  места (routes)
@routes_bp.route('/api/routes', methods=['GET', 'POST'])
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
                'photo': route.photo,
                'approved': route.approved
            }
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
            approved=False
        )
        db.session.add(new_route)
        db.session.commit()
        return jsonify({'message': 'Место успешно добавлено и ожидает модерации'}), 201

    return jsonify({'message': 'Метод не разрешен'}), 405

# Маршруты для API модерации мест
@routes_bp.route('/api/moderate', methods=['GET', 'POST'])
def moderate_routes():
    if request.method == 'GET':
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
                'photo': route.photo,
                'approved': route.approved
            }
            route_list.append(route_data)
        return jsonify(route_list)
    elif request.method == 'POST':
        data = request.get_json()
        route_id = data['id']
        action = data['action']

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

# Маршруты для регистрации и входа пользователей

@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            error = 'Пожалуйста, заполните все поля.'
        elif len(username) < 3:
            error = 'Имя пользователя должно быть не менее 3 символов.'
        elif len(password) < 6:
            error = 'Пароль должен быть не менее 6 символов.'
        else:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                error = 'Пользователь с таким именем уже существует.'
            else:
                try:
                    hashed_password = generate_password_hash(password)
                    new_user = User(username=username, password=hashed_password)
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect(url_for('routes.login'))
                except Exception as e:
                    db.session.rollback()
                    error = 'Произошла ошибка при регистрации: ' + str(e)

    return render_template('register.html', error=error)


@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('routes.index'))
        else:
            return render_template('login.html', error='Неверный логин или пароль')

    return render_template('login.html')
@routes_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('routes.login'))

# Пример главной страницы (потребуется изменить)
@routes_bp.route('/')
def index():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        if user:
            routes = Route.query.all()  # Получаем все маршруты
            return render_template('index.html', username=username, routes=routes)
        else:
            return 'Пользователь не найден', 404
    else:
        return redirect(url_for('routes.login'))

@routes_bp.route('/api/routes/<int:route_id>/reviews', methods=['GET', 'POST'])
def route_reviews(route_id):
    route = Route.query.get_or_404(route_id)

    if request.method == 'GET':
        reviews = Review.query.filter_by(route_id=route_id).all()
        review_list = []
        for review in reviews:
            review_data = {
                'id': review.id,
                'user_id': review.user_id,
                'username': review.user.username,
                'text': review.text,
                'rating': review.rating,
                'timestamp': review.timestamp.isoformat()
            }
            review_list.append(review_data)
        return jsonify(review_list)


    elif request.method == 'POST':
        if 'username' not in session:
            return jsonify({'error': 'Требуется авторизация'}), 401

        data = request.get_json()
        text = data.get('text')
        rating = data.get('rating')

        if not text or not rating:
            return jsonify({'error': "Пожалуйста, заполните все поля."}), 400

        if not (1 <= int(rating) <= 5):
            return jsonify({'error': "Оценка должна быть от 1 до 5"}), 400

        user = User.query.filter_by(username=session['username']).first()
        if not user:
            return jsonify({'error': "Пользователь не найден"}), 404

        new_review = Review(route_id=route_id, user_id=user.id, text=text, rating=rating)
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': "Отзыв успешно добавлен"}), 201
@routes_bp.route('/api/username', methods=['GET'])
def get_username():
    if 'username' in session:
        return jsonify({'username': session['username']})
    else:
        return jsonify({'username': None})

from flask import render_template, jsonify

@routes_bp.route('/render_template', methods=['POST'])
def render_template_route():
    data = request.get_json()
    template = data['template']
    context = data['data']
    return render_template(template, **context)