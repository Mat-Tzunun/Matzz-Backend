from flask import Blueprint, request
from src.db.models import Users, user_schema
from src.app import db

usersRoutes = Blueprint('users', __name__)


@usersRoutes.route('/user', methods=['POST'])
def CREATE_USER():
    username = request.json['username']
    email = request.json['email']
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
