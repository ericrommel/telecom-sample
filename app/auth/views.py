from flask import abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .. import db

from ..models import Employee


@auth.route("/register", methods=["POST"])
def register():
    """
    Handle requests to the /register route. Here an employee will be added to the database
    """

    email = request.json["email"]
    username = request.json["username"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    password = request.json["password"]
    is_admin = request.json["is_admin"]
    # password_confirm = request.json['password_confirm']

    if Employee.query.filter_by(email=email).first():
        abort(403, description=f"{email} is already in use.")

    if Employee.query.filter_by(username=username).first():
        abort(403, description=f"{username} is already in use.")

    # if password != password_confirm:
    #     abort(403, 'Username is already in use.')

    employee = Employee(
        email=email, username=username, first_name=first_name, last_name=last_name, password=password, is_admin=is_admin
    )

    db.session.add(employee)
    db.session.commit()
    print(employee)
    return jsonify(employee)


@auth.route("/login", methods=["POST"])
def login():
    """
    Handle requests to the /login route. Log an employee
    """

    email = request.json["email"]
    password = request.json["password"]

    # Check if the employee exists in the database and if the password entered matches the password in the database
    employee = Employee.query.filter_by(email=email).first()
    if employee is not None and employee.verify_password(password):
        # log employee in
        login_user(employee)

    return jsonify(employee)


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Handle requests to the /logout route. Log an employee out
    """
    logout_user()
    return jsonify({"message": "You have successfully been logged out."}), 200
