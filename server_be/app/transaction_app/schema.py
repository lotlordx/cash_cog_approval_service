from .models import TransactionModel
from app import ma
from app.employee_app.schema import EmployeeSchema
from app.currency_app.schema import CurrencySchema


class TransactionSchema(ma.ModelSchema):
    employee = ma.Nested("EmployeeSchema", only=("uuid", "first_name", "last_name"))
    currency = ma.Nested("CurrencySchema", only=("id", "currency_code"))

    class Meta:
        model = TransactionModel
