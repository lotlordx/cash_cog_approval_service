from app import db
from app.employee_app.models import EmployeeModel
from app.currency_app.models import CurrencyModel


class TransactionModel(db.Model):
    """
    This represents the transactions Model / transaction_model table.
    Field attributes declared here represents , corresponding
    column names and attributes in the db.

    This model would serve as a visual feel to the  client. Approvals
    and other crud operations would be permissible here
    """

    __tablename__ = "transaction_model"

    uuid = db.Column(db.String(100), unique=True, primary_key=True)
    amount = db.Column(db.String(200), index=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency_model.id'))
    currency = db.relationship("CurrencyModel", backref="curr_x")
    description = db.Column(db.String(200), index=True)
    employee_id = db.Column(db.String(200), db.ForeignKey('employee_model.uuid'))
    employee = db.relationship("EmployeeModel", backref="emp_x")
    status = db.Column(db.Boolean, default=True)
    approval_status = db.Column(db.String(10), default="pending")
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, uuid=None, amount=None, currency=None, description=None, employee=None, created_at=None):
        self.uuid = uuid
        self.amount = amount
        self.currency_code = currency
        self.description = description
        self.employee_details = employee
        self.created_at = created_at

    def save(self):
        """
        This function saves a transactionModel object to the db
        """
        employee = EmployeeModel(**self.employee_details)
        currency = CurrencyModel(self.currency_code)

        # check if employee record exists before making an insert
        employee_record_in_db = EmployeeModel.query.filter_by(uuid=employee.uuid).scalar()
        if employee_record_in_db is None:
            employee.save()
            self.employee_id = employee.uuid
        else:
            self.employee_id = employee_record_in_db.uuid

        # check if currency record exists before making an insert
        currency_record_in_db = CurrencyModel.query.filter_by(currency_code=self.currency_code).scalar()
        if currency_record_in_db is None:
            currency.save()
            self.currency_id = currency.id
        else:
            self.currency_id = currency_record_in_db.id

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as ex:
            db.session.rollback

    def roll_back(self):
        """
        This function rolls back a commit state in the db
        """
        db.session.rollback()

    def commit(self):
        """
        This function commits record to the active session
        :return: None
        """
        db.session.commit()
