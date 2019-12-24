from .models import CurrencyModel
from app import ma


class CurrencySchema(ma.ModelSchema):
        class Meta:
            model = CurrencyModel