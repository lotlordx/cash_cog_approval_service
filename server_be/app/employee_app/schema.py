from .models import EmployeeModel
from app import ma


class EmployeeSchema(ma.ModelSchema):
    """
    This CLass Handles the serialization and deserialization
    of the employeeModel instance. Flask Marshamallow lib calls the
    ModelSchema Class, which is  Inherited,  to perform this
    action.
    """

    class Meta:
        model = EmployeeModel
