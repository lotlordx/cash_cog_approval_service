from decouple import config

FLASK_APP = config("SECRET_KEY", default="run.py")
SECRET_KEY = config("SECRET_KEY", default="")
SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI", default="")
ENVIROMENT = config("ENVIROMENT", default="development")
BROKER_URI = config("BROKER_URI", default="localhost:9092")
SERVICE_KAFKA_TOPIC = config("SERVICE_KAFKA_TOPIC", default="approval_topic")
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="")
STREAM_URL = "https://cashcog.xcnt.io/stream"
APP_PORT = config("APP_PORT", default=5000)
