from flask import Blueprint, jsonify, request
from src.core.OpenAI import MattzunuIA
from src.app import db
from src.db.models import Exercises, exercises_schema, exercise_schema
from datetime import datetime

exercisesRoutes = Blueprint('exercises', __name__)


@exercisesRoutes.route('/exercises', methods=['POST'])
def CREATE_EXERCISE():
    try:
        mattzunu = MattzunuIA(api_key="xxxxxxxxxxxxxxxxxx")
        data = mattzunu.generate_exercise(level=1)

        if (data is None):
            return jsonify({"message": "Error: Invalid data from AI"}), 400

        if "operation" not in data or "message" not in data:
            return jsonify({"message": "Error: Invalid data from AI"}), 400

        exercise = data["operation"]
        message = data["message"]
        message_success = data["messageSuccess"]
        message_failure = data["messageFailure"]

        # Ensure exercise contains required fields
        exercise_numbers = exercise.get("numbers")
        exercise_operation = exercise.get("operation")
        exercise_result = exercise.get("result")
        exercise_level = exercise.get("level")

        if exercise_numbers is None or exercise_operation is None or exercise_result is None:
            return jsonify({"message": "Error: Missing fields in exercise data"}), 400

        new_exercise = Exercises(
            user_id=1,
            numbers=exercise_numbers,  # Ensure this is a valid format
            operation=exercise_operation,
            result=exercise_result,
            time_taken=0,
            level=exercise_level,
            resolved=False,
            message=message,
            message_success=message_success,
            message_failure=message_failure,
            solved_at=None  # Set to None initially
        )

        db.session.add(new_exercise)
        db.session.commit()

        return jsonify({
            "message": "Success creating exercise",
            "data": exercise_schema.dump(new_exercise)
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback on error
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@exercisesRoutes.route('/exercises', methods=['GET'])
def GET_EXERCISES():
    try:
        exercises = Exercises.query.all()
        print(exercises)
        return jsonify({"message": "Success getting exercises", "data": exercises_schema.dump(exercises)}), 200
    except Exception as e:
        db.session.rollback()  # Rollback on error
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@exercisesRoutes.route('/exercises_by_user/<int:user_id>', methods=['GET'])
def GET_EXERCISES_BY_USER(user_id):
    try:
        exercises = Exercises.query.filter_by(user_id=user_id).all()
        return jsonify({"message": "Success getting exercises", "data": exercises_schema.dump(exercises)}), 200
    except Exception as e:
        db.session.rollback()  # Rollback on error
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@exercisesRoutes.route('/exercises/<int:exercise_id>', methods=['GET'])
def GET_EXERCISE(exercise_id):
    try:
        exercise = Exercises.query.get(exercise_id)
        if exercise is None:
            return jsonify({"message": "Exercise not found"}), 404
        return jsonify({"message": "Success getting exercise", "data": exercise_schema.dump(exercise)}), 200
    except Exception as e:
        db.session.rollback()  # Rollback on error
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@exercisesRoutes.route('/exercises/<int:exercise_id>', methods=['PUT'])
def UPDATE_EXERCISE(exercise_id):
    try:
        exercise = Exercises.query.get(exercise_id)
        if exercise is None:
            return jsonify({"message": "Exercise not found"}), 404

        data = request.json
        if "operation" not in data or "message" not in data:
            return jsonify({"message": "Error: Invalid data from AI"}), 400

        exercise = data["operation"]
        message = data["message"]
        message_success = data["messageSuccess"]
        message_failure = data["messageFailure"]

        # Ensure exercise contains required fields
        exercise_numbers = exercise.get("numbers")
        exercise_operation = exercise.get("operation")
        exercise_result = exercise.get("result")
        exercise_level = exercise.get("level")

        if exercise_numbers is None or exercise_operation is None or exercise_result is None:
            return jsonify({"message": "Error: Missing fields in exercise data"}), 400

        exercise.numbers = exercise_numbers  # Ensure this is a valid format
        exercise.operation = exercise_operation
        exercise.result = exercise_result
        exercise.time_taken = 0
        exercise.level = exercise_level
        exercise.resolved = False
        exercise.message = message
        exercise.message_success = message_success
        exercise.message_failure = message_failure
        exercise.solved_at = None  # Set to None initially

        db.session.commit()

        return jsonify({
            "message": "Success updating exercise",
            "data": exercise_schema.dump(exercise)
        }), 200
    except Exception as e:
        db.session.rollback()  # Rollback on error
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@exercisesRoutes.route('/exercises_resolved/<int:exercise_id>', methods=['PUT'])
def UPDATE_RESOLVE_EXERCISE(exercise_id):
    try:
        exercise = Exercises.query.get(exercise_id)
        if exercise is None:
            return jsonify({"message": "Exercise not found"}), 404

        exercise.resolved = True
        exercise.solved_at = datetime.now()

        db.session.commit()

        return jsonify({
            "message": "Success updating exercise",
            "data": exercise_schema.dump(exercise)
        }), 200

    except Exception as e:
        db.session.rollback()  # Rollback on error
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
