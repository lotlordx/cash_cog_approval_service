from flask_restful import Api
from flask_cors import CORS

from app.employee_app.controller import EmployeeController
from settings.constants import ENVIROMENT, APP_PORT
from app import create_app, make_celery
from app.transaction_app.controller import TransactionListController, TransactionController, \
    TransactionAnalyticsController
from app.currency_app.controller import CurrencyController


app = create_app(ENVIROMENT)
celery = make_celery(app)
CORS(app)


rest_route = Api(app, '/api/v1')
rest_route.add_resource(TransactionListController, '/transactions')
rest_route.add_resource(TransactionController, '/transactions/<trans_id>')
rest_route.add_resource(TransactionAnalyticsController, '/transactions/analytics')
rest_route.add_resource(CurrencyController, '/currency')
rest_route.add_resource(EmployeeController, '/employee')

if __name__ == "__main__":
    from tools.celery.tasks import kafka_producer
    kafka_producer.delay()

    app.run(host='0.0.0.0', port=APP_PORT)
