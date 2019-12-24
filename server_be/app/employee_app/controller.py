from flask_restful import Resource

from .services import EmployeeServices


class EmployeeController(Resource):
    """
    This class handles all incoming requests
    and return its appropriate response
    """

    def __init__(self):
        self._services = EmployeeServices()

    def get(self):
        """
            This function handles the get requests made
            to this controller
        :return: json response
        """
        response = self._services.get_all(
        response.status_code = 200
        return response


