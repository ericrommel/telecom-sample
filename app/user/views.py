import json
import sqlite3

import sqlalchemy
from flask import abort, jsonify, request, url_for
from flask_login import current_user, login_required
from marshmallow_sqlalchemy import exceptions
from sqlalchemy import exc
from sqlalchemy.exc import OperationalError, IntegrityError, InvalidRequestError, SQLAlchemyError

from . import user
from .. import db
from ..models import DidNumber, did_number_schema, did_numbers_schema, Employee, employee_schema, employees_schema
from log import Log

log = Log("evolux-project").get_logger(logger_name="user-views")


def check_admin():
    """
    Prevent non-admins from accessing the page
    """

    if not current_user.is_admin:
        abort(403, "The current user is not an admin")


def get_paginated_list(klass, url: str, start: int, limit: int) -> dict:
    """
    Paginate response.
    Based on: https://aviaryan.com/blog/gsoc/paginated-apis-flask
    """

    # check if page exists
    results = klass
    count = len(results)
    if not isinstance(start, int):
        start = int(start)

    if not isinstance(limit, int):
        limit = int(limit)

    if count < start:
        abort(404)

    # make response
    obj = {"start": start, "limit": limit, "count": count}

    log.info("Build the urls to return")
    # make previous url
    if start == 1:
        obj["previous"] = ""
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj["previous"] = url + "?start=%d&limit=%d" % (start_copy, limit_copy)

    # make next url
    if start + limit > count:
        obj["next"] = ""
    else:
        start_copy = start + limit
        obj["next"] = url + "?start=%d&limit=%d" % (start_copy, limit)

    log.info("Extract result according to the bounds")
    obj["results"] = results[(start - 1) : (start - 1 + limit)]
    return obj


# DID number views
@user.route("/didnumbers")
@user.route("/didnumbers/page/<int:page>")
@login_required
def list_didnumbers(page=1, per_page=20):
    """
    List all DID numbers
    """

    try:
        log.info("Get the list of DID numbers from the database")
        all_did_numbers = did_numbers_schema.dump(DidNumber.query.order_by(DidNumber.id.asc()))
    except OperationalError:
        log.info("There is no DID numbers in the database")
        all_did_numbers = None

    if all_did_numbers is None:
        return jsonify({"warning": "There is no data to show"})

    data = get_paginated_list(
        klass=all_did_numbers,
        url=url_for("user.list_didnumbers"),
        start=request.args.get("start", page),
        limit=request.args.get("limit", per_page),
    )

    log.info("Response the list of DID numbers")
    return jsonify(data)


@user.route("/didnumbers/<int:id>", methods=["GET"])
@login_required
def didnumber_detail(id):
    """
    List details for a DID number
    """

    did_number = DidNumber.query.get_or_404(id)
    return did_number_schema.jsonify(did_number)


@user.route("/didnumbers/add", methods=["GET", "POST"])
@login_required
def add_didnumber():
    """
    Add a DID number to the database
    """

    log.info("Set variables from request")
    value, monthly_price, setup_price, currency = "", "", "", ""
    try:
        value = request.json["value"]
        monthly_price = request.json["monthlyPrice"]
        setup_price = request.json["setupPrice"]
        currency = request.json["currency"]
    except KeyError as e:
        abort(400, f"There is no key with that value: {e}")

    did_number = DidNumber(
        value=value,
        monthly_price=monthly_price,
        setup_price=setup_price,
        currency=currency,
    )

    try:
        # Add DID number to the database
        log.info(f"Add DID number {did_number.value} to the database")
        db.session.add(did_number)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(403, f"DID Number value {did_number.value} already exists in the database.")
    except Exception as e:
        abort(500, e)

    return did_number_schema.jsonify(did_number), 201


@user.route("/didnumbers/edit/<int:id>", methods=["GET", "PUT"])
@login_required
def edit_did_number(id):
    """
    Edit a DID number
    """

    check_admin()

    did_number = DidNumber.query.get_or_404(id)
    log.info("Set variables from request")
    try:
        did_number.value = request.json["value"]
        did_number.monthly_price = request.json["monthlyPrice"]
        did_number.setup_price = request.json["setupPrice"]
        did_number.currency = request.json["currency"]
    except KeyError as e:
        abort(400, f"There is no key with that value: {e}")

    try:
        # Edit DID number in the database
        log.info(f"Edit DID number {did_number.value} in the database")
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(400, f"DID Number value {did_number.value} already exists.")
    except Exception as e:
        abort(500, e)

    return did_number_schema.jsonify(did_number), 200


@user.route("/didnumbers/delete/<int:id>", methods=["GET", "DELETE"])
@login_required
def delete_did_number(id):
    """
    Delete a DID number from the database
    """

    check_admin()

    did_number = DidNumber.query.get_or_404(id)
    try:
        log.info(f"Delete {did_number} from the database")
        db.session.delete(did_number)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(400, f"DID Number value {did_number.value} already deleted.")
    except Exception as e:
        abort(500, e)

    return jsonify({"message": "The DID number has successfully been deleted."}), 200


# Employee views
@user.route("/employees")
@login_required
def list_employees():
    """
    List all employees
    """

    check_admin()

    log.info("List all employees")
    all_employees = Employee.query.all()

    result = employees_schema.dump(all_employees)
    return jsonify(result), 200


@user.route("/employees/<int:id>")
@login_required
def employee_detail(id):
    """
    List details for an employee
    """

    check_admin()
    employee = Employee.query.get_or_404(id)
    return employee_schema.jsonify(employee)
