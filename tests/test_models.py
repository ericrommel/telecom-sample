from app.models import Employee, DidNumber


def test_employee_model(app):
    """
    Test number of records in Employee table
    """

    assert Employee.query.count() == 2


def test_did_number_model(app):
    """
    Test number of records in DID Numbers table
    """

    assert DidNumber.query.count() == 2
