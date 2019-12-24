from .models import EmployeeModel
from app import ma


class EmployeeSchema(ma.ModelSchema):
        class Meta:
            model = EmployeeModel
