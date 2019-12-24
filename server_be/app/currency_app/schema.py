from .models import CurrencyModel
from app import ma


class CurrencySchema(ma.ModelSchema):
    """
    This CLass Handles the serialization and deserialization
    of the currencymodel instance. Flask Marshamallow lib
    ModelSchema Class was Inherited to perform this
    action.
    """
    class Meta:
        model = CurrencyModel