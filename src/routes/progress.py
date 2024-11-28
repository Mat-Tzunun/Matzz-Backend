from src.app import app, db
from flask import Blueprint, request, jsonify
from src.db.models import Progress, Exercises, progress_schema
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

progressRoutes = Blueprint('progress', __name__)


@progressRoutes.route("/progress/<int:id_user>", methods=["GET"])
def GET_PROGRESS(id_user):
    try:
        progress = Progress.query.filter(Progress.user_id == id_user).first()
        if not progress:
            return jsonify({"message": "No progress found for this user"}), 404

        new_schema = progress_schema.dump(progress)
        return jsonify({"message": "Progress user Success", "data": new_schema}), 200
    except SQLAlchemyError as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), 500


@progressRoutes.route('/progress/<int:id_user>', methods=['POST'])
def CREATE_PROGRESS(id_user):
    try:
        data = request.json
        if not data or 'current_level' not in data:
            return jsonify({"message": "Invalid input"}), 400

        level = data["current_level"]
        progress = Progress.query.filter_by(user_id=id_user).first()

        exercises = Exercises.query.filter(
            Exercises.user_id == id_user, Exercises.resolved == True).all()
        numExercises = len(exercises)

        if progress:
            progress.current_level = level
            progress.exercises_solved = numExercises
            progress.last_updated = datetime.now()
        else:
            progress = Progress(user_id=id_user, current_level=level,
                                exercises_solved=numExercises, last_updated=datetime.now())
            db.session.add(progress)

        db.session.commit()
        return jsonify({"message": "Success", "data": progress_schema.dump(progress)}), 201
    except SQLAlchemyError as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), 500
