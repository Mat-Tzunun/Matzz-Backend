from src.app import db, ma
from sqlalchemy.dialects.mysql import JSON


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email')


class Exercises(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    numbers = db.Column(JSON, nullable=False)
    operation = db.Column(db.String(80), nullable=False)
    result = db.Column(db.String(80), nullable=False)
    time_taken = db.Column(db.Integer, nullable=True)
    level = db.Column(db.Integer, nullable=False)
    resolved = db.Column(db.Boolean, nullable=False)
    message = db.Column(db.String(80), nullable=False)
    message_success = db.Column(db.String(80), nullable=False)
    message_failure = db.Column(db.String(80), nullable=False)
    solved_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, user_id: int, operation: str, result: str, time_taken: int, level: int, resolved: bool, numbers: list, message: str, message_success: str, message_failure: str, solved_at: str = None):
        self.user_id = user_id
        self.operation = operation
        self.result = result
        self.time_taken = time_taken
        self.level = level
        self.resolved = resolved
        self.numbers = numbers
        self.message = message
        self.message_success = message_success
        self.message_failure = message_failure
        self.solved_at = solved_at


class ExercisesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'numbers', 'operation', 'result',
                  'time_taken', 'level', 'resolved', 'message', 'message_success', 'message_failure', 'solved_at')


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exercises_solved = db.Column(db.Integer, nullable=False)
    current_level = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id: int, exercises_solved: int, current_level: int, last_updated: str):
        self.user_id = user_id
        self.exercises_solved = exercises_solved
        self.current_level = current_level
        self.last_updated = last_updated


class ProgressSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'exercises_solved',
                  'current_level', 'last_updated')


# Instancias de los modelos
user_schema = UsersSchema()
exercise_schema = ExercisesSchema()
exercises_schema = ExercisesSchema(many=True)
progress_schema = ProgressSchema()
