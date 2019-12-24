from app import db


class EmployeeModel(db.Model):
    """
    This represents the Employee Model / Employee_model table.
    Field attributes declared here represents , corresponding
    column names and attributes in the db.
    """

    __tablename__ = 'employee_model'

    uuid = db.Column(db.String(200), primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))

    def __init__(self, uuid, first_name, last_name):
        self.uuid = uuid
        self.first_name = first_name
        self.last_name = last_name

    def save(self):
        """
        This function saves an employeeModel object to the db
        """
        try:
            db.session.add(self)
            db.session.flush()
        except Exception as ex:
            self.roll_back()

    @staticmethod
    def roll_back():
        """
        This function rolls back a commit state in the db
        """
        db.session.rollback()

