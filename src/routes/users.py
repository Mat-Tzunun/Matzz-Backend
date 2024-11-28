from flask import Blueprint, request
from src.db.models import Users, user_schema
from src.app import db

usersRoutes = Blueprint('users', __name__)


@usersRoutes.route('/user', methods=['POST'])
def CREATE_USER():
    username = request.json['username']
    email = request.json['email']

    # Verificar si el usuario ya existe
    existing_user = Users.query.filter(
        (Users.username == username) | (Users.email == email)).first()

    if existing_user:
        # Si el usuario ya existe, devolver el usuario existente
        return user_schema.jsonify(existing_user)

    # Si no existe, crear un nuevo usuario
    new_user = Users(username, email)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


@usersRoutes.route('/user/<int:id>', methods=['GET'])
def GET_USER(id):
    user = Users.query.get(id)
    if user is None:
        return {'message': 'User not found'}, 404
    return user_schema.jsonify(user)
