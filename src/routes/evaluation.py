from flask import Blueprint, request, jsonify
from src.db.models import Exercises, exercise_schema, Progress
from src.core.AI import Prediccion

evaluationRoutes = Blueprint('evaluation', __name__)


@evaluationRoutes.route('/evaluation_exercise/<int:exercise_id>', methods=['POST'])
def CREATE_EVALUATION(exercise_id):
    try:
        # Check if the request body contains 'result'
        if not request.json or 'result' not in request.json:
            return jsonify({"message": "Missing 'result' in request body"}), 400

        user_result = request.json.get("result")

        # Fetch exercise from the database
        exercise_by_id = Exercises.query.get(exercise_id)

        if exercise_by_id is None:
            return {
                "message": "Exercise not found",
                "data": {
                    "resolved": False,
                    "message": "No message available"
                }
            }, 404

        # Serialize the exercise object
        exercise_data = exercise_schema.dump(exercise_by_id)

        exercise_result = exercise_data.get("result")
        exercise_message_success = exercise_data.get("message_success")
        exercise_message_failure = exercise_data.get("message_failure")

        # Ensure user_result is compared as the same type as exercise_result
        try:
            if isinstance(exercise_result, (int, float)):
                user_result = float(user_result) if '.' in str(
                    user_result) else int(user_result)
            elif isinstance(exercise_result, str):
                user_result = str(user_result).strip()
        except ValueError:
            return {
                "message": "Invalid result format",
                "data": {
                    "resolved": False,
                    "message": exercise_message_failure
                }
            }, 202

        print("--------------------------------------------")
        print("Resultados: ", exercise_result, user_result)
        print(type(exercise_result), type(user_result))
        print(exercise_result == user_result)
        print("--------------------------------------------")

        # Check if the user's result matches the expected result
        if exercise_result != user_result:
            return {
                "message": "Exercise not resolved",
                "data": {
                    "resolved": False,
                    "message": exercise_message_failure
                }
            }, 201

        return {
            "message": "Exercise resolved",
            "data": {
                "resolved": True,
                "message": exercise_message_success
            }
        }, 200

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@evaluationRoutes.route("/evaluation/prediction/<int:id_user>", methods=['GET'])
def EVALUATION_PREDICTION(id_user):
    try:
        # Obtener los ejercicios del usuario específico
        exercises = Exercises.query.filter_by(user_id=id_user).all()

        # Obtener el progreso del usuario
        progress = Progress.query.filter_by(user_id=id_user).first()

        if progress is None:
            return jsonify({"message": "User progress not found"}), 404

        exercises_solver = progress.exercises_solved
        exercises_not_solved = len(exercises) - exercises_solver
        level_current = progress.current_level
        newTupla = (level_current, 5.2, exercises_solver, exercises_not_solved)

        # Predicción
        modelo = Prediccion()
        predict = modelo.predecir(newTupla)

        return jsonify({
            "message": "Success",
            "data": {
                "predict": predict
            }
        }), 200

    except Exception as e:
        # Imprimir el error para depuración
        print("Error Server:", e)
        return jsonify({"message": "Error", "error": str(e)}), 500
