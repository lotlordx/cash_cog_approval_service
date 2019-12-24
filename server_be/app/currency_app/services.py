from typing import List
from flask import jsonify
from .schema import CurrencySchema
from .models import CurrencyModel


class CurrencyServices:
    """
    This Class Handles all Currency
    related business Logics.
    """

    def __init__(self):
        self.service_model = CurrencyModel

    def get_all(self) -> List[CurrencyModel]:
        """
        This function fetches all currency records
        from the database.
        For optimisation only needed fields are loaded
        upon query
        :return json currencyModel object:
        """
        query_result = self.service_model.query.with_entities(self.service_model.id, self.service_model.currency_code)
        schema = CurrencySchema(many=True)
        result = schema.dump(query_result)
        return jsonify({"currency_list": result})
