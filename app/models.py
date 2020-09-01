from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager, ma
from log import Log

log = Log("evolux-project").get_logger(logger_name="models")


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)

    def check_password(self, password):
        """
        Check if hashed password matches with actual password
        """

        log.info(f"Verify password: {self.password_hash} - {password}")
        return check_password_hash(self.password_hash, password)

    def __init__(self, first_name, last_name, email, username, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return f"<Employee: {self.username}>"


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        fields = ("first_name", "last_name", "email", "username", "is_admin")
        model = Employee
        load_instance = True


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    log.info("Set up an user loader")
    return Employee.query.get(int(user_id))


class DidNumber(db.Model):
    """
    Create a DID Number table
    """

    __tablename__ = "didnumbers"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(17), unique=True)
    monthly_price = db.Column(db.Float)
    setup_price = db.Column(db.Float)
    currency = db.Column(db.String(3))

    def __init__(self, value, monthly_price, setup_price, currency):
        log.info("Create a DID number instance")
        self.value = value
        self.monthly_price = monthly_price
        self.setup_price = setup_price
        self.currency = currency

    def __repr__(self):
        return f"<DIDNumber: {self.value}>"


class DidNumberSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("value", "monthly_price", "setup_price", "currency")
        model = DidNumber
        load_instance = True


did_number_schema = DidNumberSchema()
did_numbers_schema = DidNumberSchema(many=True)
