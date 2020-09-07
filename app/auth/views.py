from flask import abort, jsonify, request
from flask_login import login_required, login_user, logout_user

from log import Log
from . import auth
from .. import db
from ..models import Employee, employee_schema

log = Log("evolux-project").get_logger(logger_name="auth-views")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle requests to the /register route. Here an user will be added to the database
    """

    log.info("Set employee variables from request")
    email, username, first_name, last_name, password, is_admin = "", "", "", "", "", ""
    try:
        email = request.json["email"]
        username = request.json["username"]
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        password = request.json["password"]
        is_admin = request.json["is_admin"]
    except KeyError as e:
        log.error(f"KeyError: {e}")
        abort(400, f"There is no key with that value: {e}")

    if Employee.query.filter_by(email=email).first():
        log.error(f"{email} is already in use.")
        abort(403, description=f"{email} is already in use.")

    if Employee.query.filter_by(username=username).first():
        log.error(f"{username} is already in use.")
        abort(403, description=f"{username} is already in use.")

    employee = Employee(
        email=email, username=username, first_name=first_name, last_name=last_name, password=password, is_admin=is_admin
    )

    log.info(f'Add "{employee}" to database')
    db.session.add(employee)
    db.session.commit()

    result = employee_schema.dump(employee)
    return jsonify(result), 201


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle requests to the /login route. Log an user
    """

    if request.method == "POST":
        log.info("Set email and password from request")
        email, password = "", ""
        try:
            email = request.json["email"]
            password = request.json["password"]
        except KeyError as e:
            log.error(f"KeyError: {e}")
            abort(400, f"There is no key with that value: {e}")

        # Check if the user exists in the database and if the password entered matches the password in the database
        log.info(f"Check DB for {email}")
        employee = Employee.query.filter_by(email=email).first()
        result = ""
        if employee is not None and employee.check_password(password):
            log.info(f"{employee.username} found. Logging in")
            result = employee_schema.dump(employee)
            # log user in
            login_user(employee)
        else:
            abort(401, "Invalid email or password.")

        return jsonify(result), 200
    else:
        abort(401, "It looks like you are not logged in yet.")


@auth.route("/logout")
@login_required
def logout():
    """
    Handle requests to the /logout route. Log an user out
    """

    logout_user()
    return jsonify({"message": "You have successfully been logged out."}), 200
