from src.app import app
from src.app import db
from src.routes.users import usersRoutes
from src.routes.exercises import exercisesRoutes
from src.routes.evaluation import evaluationRoutes
from src.routes.progress import progressRoutes
from config import debug_mode, app_port

app.register_blueprint(exercisesRoutes, url_prefix='/api')
app.register_blueprint(usersRoutes, url_prefix='/api')
app.register_blueprint(evaluationRoutes, url_prefix='/api')
app.register_blueprint(progressRoutes, url_prefix='/api')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=app_port, debug=debug_mode)
