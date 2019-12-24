from app import db


class CurrencyModel(db.Model):

    __tablename__ = 'currency_model'

    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(5), unique=True)

    def __init__(self, currency):
        self.currency_code = currency

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            self.roll_back()

    @staticmethod
    def roll_back():
        db.session.rollback()
