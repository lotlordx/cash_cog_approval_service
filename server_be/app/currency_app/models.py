from app import db


class CurrencyModel(db.Model):
    """
    This represents the currency Model / currency table.
    Field attributes declared here represents , corresponding
    column names and attributes in the db.
    """

    __tablename__ = "currency_model"

    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(5), unique=True)

    def __init__(self, currency):
        self.currency_code = currency

    def save(self):
        """
        This function saves a currencyModel object to the db
        """

        try:
            db.session.add(self)
            db.session.commit()
        except:
            self.roll_back()

    @staticmethod
    def roll_back():
        """
        This function rolls back a commit state in the db
        """
        db.session.rollback()
