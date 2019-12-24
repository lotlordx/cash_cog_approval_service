from flask_api import FlaskAPI
from celery import Celery
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings.config import app_config
from settings.constants import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config: str) -> object:
    """
    This function instanciates and returns a flask api object,
    embedding other required services withing.

    :param config: Represents the enviroment the app is to run on (eg development, testing, production)
    :return: flaskapp
    """
    global app
    from app import app_loader

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.update(CELERY_BROKER_URL=CELERY_BROKER_URL, CELERY_RESULT_BACKEND=CELERY_RESULT_BACKEND)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    return app


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    celery.config_from_object(app_config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


