from flask import abort, jsonify, request
from flask_login import current_user, login_required

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
        abort(403)


# DID number views
@user.route("/didnumbers", methods=["GET"])
@login_required
def list_didnumbers():
    """
    List all DID numbers
    """

    log.info("Return the list of DID numbers")
    all_did_numbers = DidNumber.query.all()

    result = did_numbers_schema.dump(all_did_numbers)
    return jsonify(result), 200


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
    value = request.json["value"]
    monthly_price = request.json["monthlyPrice"]
    setup_price = request.json["setupPrice"]
    currency = request.json["currency"]

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
    except Exception:
        # in case DID number value already exists
        log.error(f"DID number value {value} already exists in the database")
        abort(403, "DID Number value already exists in the database.")

    # result = did_number_schema.dump(did_number)
    # return jsonify(result), 201
    return did_number_schema.jsonify(did_number), 201


@user.route("/didnumbers/edit/<int:id>", methods=["PUT"])
@login_required
def edit_did_number(id):
    """
    Edit a DID number
    """

    check_admin()

    did_number = DidNumber.query.get_or_404(id)
    log.info("Set variables from request")
    did_number.value = request.json["value"]
    did_number.monthly_price = request.json["monthlyPrice"]
    did_number.setup_price = request.json["setupPrice"]
    did_number.currency = request.json["currency"]

    try:
        # Edit DID number in the database
        log.info(f"Edit DID number {did_number.value} in the database")
        db.session.commit()
    except Exception:
        # in case DID number value already exists
        log.error(f"DID Number value {did_number.value} already exists.")
        abort(403, "DID Number value already exists.")

    # result = did_number_schema.dump(did_number)
    # return jsonify(result), 200
    return did_number_schema.jsonify(did_number), 200


@user.route("/didnumbers/delete/<int:id>", methods=["DELETE"])
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
    except Exception as e:
        log.error(f"An exception occurred: {e}")
        abort(500, "An exception occurred")

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
