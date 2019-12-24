from celery.schedules import crontab

from .constants import SQLALCHEMY_DATABASE_URI, CELERY_BROKER_URL, CELERY_RESULT_BACKEND


class BaseConfig:
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND
    CELERY_BROKER_URL = CELERY_BROKER_URL
    CSRF_ENABLE = True
    CELERY_IMPORTS = ('tools.celery.tasks')
    CELERY_TASK_RESULT_EXPIRES = 30
    CELERY_TIMEZONE = 'UTC'

    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    CELERYBEAT_SCHEDULE = {
        'perform_task': {
            'task': 'tools.celery.tasks.publish_to_db',
            # Every minute
            'schedule': crontab(minute="*"),
        },

    }


class ProductionConfig(BaseConfig):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    pass


class StagingConfig(BaseConfig):
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql://root:password@localhost/test_db"
    TESTING = True


app_config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "staging": StagingConfig,
    "testing": TestingConfig
}