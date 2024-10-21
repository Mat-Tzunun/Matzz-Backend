from flask import Blueprint, request
from src.db.models import Exercises, exercise_schema

evaluationRoutes = Blueprint('evaluation', __name__)


@evaluationRoutes.route('/evaluation_exercise/<int:exercise_id>', methods=['POST'])
def CREATE_EVALUATION(exercise_id):
    user_result = request.json["result"]

    exercise_by_id = Exercises.query.get(exercise_id)
    exercise = exercise_schema(exercise)
    exercise_result = exercise.result
    exercise_message_success = exercise.message_success
    exercise_message_failure = exercise.message_failure
    exercise_message = exercise.message

    if (exercise_by_id is None):
        return {
            "message": "Exercise not found",
            "data": {
                "resolved": False,
                "message": exercise_message
            }
        }, 404

    if (exercise_result != user_result):
        return {
            "message": "Exercise not resolved",
            "data": {
                "resolved": False,
                "message": exercise_message_failure
            }
        }, 400

    return {
        "message": "Exercise resolved",
        "data": {
            "resolved": True,
            "message": exercise_message_success
        }
    }
