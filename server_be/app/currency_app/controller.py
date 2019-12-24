from flask_restful import Resource
from .services import CurrencyServices


class CurrencyController(Resource):
    """
    This class handles all incoming requests
    and return its appropriate response
    """

    def __init__(self):
        self._services = CurrencyServices()

    def get(self):
        response = self._services.get_all()
        response.status_code = 200
        return response


