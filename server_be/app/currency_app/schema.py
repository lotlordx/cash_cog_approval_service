from .models import CurrencyModel
from app import ma


class CurrencySchema(ma.ModelSchema):
    """
    This CLass Handles the serialization and deserialization
    of the currencymodel instance. Flask Marshamallow lib calls the
    ModelSchema Class, which is  Inherited,  to perform this
    action.
    """

    class Meta:
        model = CurrencyModel
