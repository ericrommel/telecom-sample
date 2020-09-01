from flask import abort, flash, jsonify, request
from flask_login import login_required, login_user, logout_user

from . import auth
from .. import db

from ..models import Employee, employee_schema
from log import Log

log = Log("evolux-project").get_logger(logger_name="views")


@auth.route("/signup", methods=["POST"])
def signup():
    """
    Handle requests to the /register route. Here an employee will be added to the database
    """

    log.info("Set variables from request")
    email = request.json["email"]
    username = request.json["username"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    password = request.json["password"]
    is_admin = request.json["is_admin"]
    # password_confirm = request.json['password_confirm']

    if Employee.query.filter_by(email=email).first():
        log.error(f"{email} is already in use.")
        abort(403, description=f"{email} is already in use.")

    if Employee.query.filter_by(username=username).first():
        log.error(f"{username} is already in use.")
        abort(403, description=f"{username} is already in use.")

    log.info("Create an Employee instance")
    employee = Employee(
        email=email, username=username, first_name=first_name, last_name=last_name, password=password, is_admin=is_admin
    )

    log.info(f'Add "{employee}" to database')
    db.session.add(employee)
    db.session.commit()

    result = employee_schema.dump(employee)
    return jsonify(result), 201


@auth.route("/login", methods=["POST"])
def login():
    """
    Handle requests to the /login route. Log an employee
    """

    log.info("Set variables from request")
    email = request.json["email"]
    password = request.json["password"]

    # Check if the employee exists in the database and if the password entered matches the password in the database
    log.info(f"Check DB for {email}")
    employee = Employee.query.filter_by(email=email).first()
    result = ""
    if employee is not None and employee.check_password(password):
        log.info(f"{employee.username} found. Logging in")
        result = employee_schema.dump(employee)
        # log employee in
        login_user(employee)

    return jsonify(result), 200


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Handle requests to the /logout route. Log an employee out
    """

    logout_user()
    return jsonify({"message": "You have successfully been logged out."}), 200
