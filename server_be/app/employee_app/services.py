from typing import List
from flask import jsonify
from .schema import EmployeeSchema
from .models import EmployeeModel


class EmployeeServices:
    """
    This Class Handles all Employee
    related business Logics.
    """

    def __init__(self):
        self.service_model = EmployeeModel

    def get_all(self) -> List[EmployeeModel]:
        """
        This function fetches all employee records
        from the database.
        For optimisation only needed fields are loaded
        upon query
        :return json employeeModel object:
        """

        query_result = self.service_model.query.with_entities(self.service_model.uuid, self.service_model.first_name,
                                                              self.service_model.last_name)
        schema = EmployeeSchema(many=True)
        result = schema.dump(query_result)
        return jsonify({"employee_list": result})


