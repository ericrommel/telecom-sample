import json
import os
import string
from random import choice

import pytest
from flask import url_for

from app import create_app, db
from app.models import Employee, DidNumber


def get_url(app, url, next_url=None, id=None):
    with app.test_request_context():
        return url_for(url, next=next_url, id=id)


class AuthActions(object):
    def __init__(self, app, client):
        self._app = app
        self._client = client

    def signup(self, a_dict):
        """
        Sign up request
        """

        return self._client.post(
            get_url(app=self._app, url="auth.signup"),
            data=json.dumps(a_dict),
            content_type="application/json",
            follow_redirects=True,
        )

    def login(self, a_dict):
        """
        Logo in request
        """

        return self._client.post(
            get_url(app=self._app, url="auth.login"),
            data=json.dumps(a_dict),
            content_type="application/json",
            follow_redirects=True,
        )

    def logout(self):
        """
        Log out request
        """

        return self._client.get(get_url(app=self._app, url="auth.logout"), follow_redirects=True)

    def generic_put(self, url, a_dict):
        """
        Generic PUT request
        """

        return self._client.put(url, data=json.dumps(a_dict), content_type="application/json", follow_redirects=True)

    def generic_post(self, url, a_dict):
        """
        Generic POST request
        """

        return self._client.post(url, data=json.dumps(a_dict), content_type="application/json", follow_redirects=True)


@pytest.fixture
def auth(app, client):
    return AuthActions(app, client)


@pytest.fixture()
def app():
    """
    Create app with a database test
    """

    # project_dir = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///'telecom-test.db'}"

    app = create_app()
    app.config.from_object("config.TestingConfig")
    app.config.update(SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI)
    app.config.update(PRESERVE_CONTEXT_ON_EXCEPTION=False)

    with app.app_context():
        # Will be called before every test
        db.create_all()

        # Create test admin user
        admin = Employee(
            username="admin",
            password="123456",
            is_admin=True,
            first_name="First Name",
            last_name="Last Name",
            email="admin@admin.com",
        )

        # Create test non-admin user
        employee = Employee(
            username="non-admin",
            password="123456",
            is_admin=False,
            first_name="First Name",
            last_name="Last Name",
            email="non-admin@admin.com",
        )

        # Create 2 DID numbers
        did_number_1 = DidNumber(
            value="+55 84 91234-4320",
            monthly_price="0.06",
            setup_price="3.49",
            currency="U$",
        )

        did_number_2 = DidNumber(
            value="+55 84 91234-4321",
            monthly_price="0.06",
            setup_price="3.49",
            currency="U$",
        )

        # Save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.add(did_number_1)
        db.session.add(did_number_2)
        db.session.commit()

        yield app

        # Will be called after every test
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """
    Make requests to the application without running the server
    """

    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def json_of_response(response):
    """
    Decode json from response
    """

    return json.loads(response.data.decode("utf8"))


def get_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    a_string = "".join(choice(letters) for i in range(length))
    return a_string


def get_random_int(length: int) -> int:
    if length > 10:
        length = 10

    numbers = "0123456789"
    a_string = "".join(choice(numbers) for i in range(length))
    return int(a_string)


def populate_did_numbers(n):
    for i in range(n):
        number = f"+55 {get_random_int(2)} {get_random_int(4)-get_random_int(4)}"
        did_number = DidNumber(
            value=number,
            monthly_price="0.06",
            setup_price="3.49",
            currency="U$",
        )
        # save users to database
        try:
            db.session.add(did_number)
            db.session.commit()
        except Exception as e:
            print(e)


def populate_employee(n):
    for i in range(n):
        username = get_random_string(10)
        email = f"{username}@gmail.com"
        employee = Employee(
            username=username,
            password="123456",
            is_admin=False,
            first_name="First Name",
            last_name="Last Name",
            email=email,
        )

        # save users to database
        try:
            db.session.add(employee)
            db.session.commit()
        except Exception as e:
            print(e)
