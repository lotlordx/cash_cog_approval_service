from flask_restful import Resource

from .services import EmployeeServices


class EmployeeController(Resource):

    def __init__(self):
        self._services = EmployeeServices()

    def get(self):
        response = self._services.get_all()
        response.status_code = 200
        return response


