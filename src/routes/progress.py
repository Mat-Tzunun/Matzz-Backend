from flask import Blueprint

progressRoutes = Blueprint('progress', __name__)


@progressRoutes.route('/progress', methods=['POST'])
def CREATE_PROGRESS():
    return "Success"
