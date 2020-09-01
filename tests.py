import unittest
import os
from flask import abort, url_for
from flask_testing import TestCase

from app.models import Employee, DidNumber
from app.user import views
from app.auth import views


class TestBase(TestCase):
    def create_app(self):
        """
        Create app with a database test
        """

        # Pass in test configurations
        config_name = "testing"
        app_test = create_app(config_name)
        project_dir = os.path.dirname(os.path.abspath(__file__))
        SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(project_dir, "telecom-test.db"))

        app_test.config.update(SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI)

        return app_test

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = Employee(
            username="admin",
            password="123456",
            is_admin=True,
            first_name="First Name",
            last_name="Last Name",
            email="admin@admin.com",
        )

        # create test non-admin user
        employee = Employee(
            username="non-admin",
            password="123456",
            is_admin=False,
            first_name="First Name",
            last_name="Last Name",
            email="non-admin@admin.com",
        )

        # create 2 DID numbers
        did_number_1 = DidNumber(
            value="+55 84 91234-4320",
            monthly_price="0.06",
            setup_price="3.49",
            currency="U$",
        )

        did_number_2 = DidNumber(
            value="+55 84 91234-4320",
            monthly_price="0.06",
            setup_price="3.49",
            currency="U$",
        )

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.add(did_number_1)
        db.session.add(did_number_2)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
    def test_employee_model(self):
        """
        Test number of records in Employee table
        """

        self.assertEqual(Employee.query.count(), 2)

    def test_did_number_model(self):
        """
        Test number of records in DID Numbers table
        """

        self.assertEqual(DidNumber.query.count(), 2)


class TestViews(TestBase):
    def test_login_view(self):
        """
        Test that login page is accessible without login
        """

        response = self.client.get(url_for("auth.login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Test that logout link is inaccessible without login and redirects to login page then to logout
        """

        target_url = url_for("auth.logout")
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_employees_view(self):
        """
        Test that employees page is inaccessible without login and redirects to login page then to employees page
        """

        target_url = url_for("user.list_employees")
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):
    def test_403_forbidden(self):
        """
        Create route to abort the request with the 403 Error
        """

        @self.app.route("/403")
        def forbidden_error():
            abort(403)

        response = self.client.get("/403")
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in str(response.data))

    def test_404_not_found(self):
        """
        Access a page that does not exist
        """

        response = self.client.get("/notexistpage")
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in str(response.data))

    def test_500_internal_server_error(self):
        """
        Create route to abort the request with the 500 Error
        """

        @self.app.route("/500")
        def internal_server_error():
            abort(500)

        response = self.client.get("/500")
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in str(response.data))


if __name__ == "__main__":
    unittest.main()
