from flask import request
from flask_restful import Resource

from .services import TransactionServices


class TransactionListController(Resource):
    """
    This class handles all incoming requests
    and return its appropriate response
    """

    def __init__(self):
        self._services = TransactionServices()

    def get(self):
        """
            This function handles the get requests made
            to this controller
        :return: json response
        """
        response = self._services.get_all_records(request)
        response.status_code = 200
        return response

    def post(self):
        """
            This function handles the post requests made
            to this controller
        :return: json response
        """
        response = self._services.create_record(request)
        response.status_code = 201
        return response


class TransactionController(Resource):
    """
    This class handles all incoming requests
    and return its appropriate response
    """

    def __init__(self):
        self._services = TransactionServices()

    def put(self, trans_id=None):
        """
            This function handles the put/update requests made
            to this controller
        :return: json response
        """
        response = self._services.update_record(request, trans_id)
        response.status_code = 200
        return response

    def delete(self, trans_id=None):
        """
            This function handles the delete requests made
            to this controller
        :return: json response
        """
        response = self._services.delete_record(request, trans_id)
        response.status_code = 200
        return response


class TransactionAnalyticsController(Resource):
    """
    This class handles all incoming requests
    and return its appropriate response
    """

    def __init__(self):
        self._services = TransactionServices()

    def get(self):
        """
            This function handles the get requests made
            to this controller
        :return: json response
        """
        response = self._services.get_analytics_record()
        response.status_code = 200
        return response


