import json
import logging
import unittest
import os
from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import Employee, DidNumber


class TestBase(TestCase):
    def create_app(self):
        """
        Create app with a database test
        """

        # Pass in test configurations
        config_name = "testing"
        app_test = create_app(config_name)
        project_dir = os.path.dirname(os.path.abspath(__file__))
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(project_dir, 'telecom-test.db')}"

        app_test.config.update(SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI)
        app_test.config.update(PRESERVE_CONTEXT_ON_EXCEPTION=False)

        return app_test

    def setUp(self):
        """
        Will be called before every test
        """

        logging.disable(logging.CRITICAL)

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
            value="+55 84 91234-4321",
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
        # logging.disable(logging.NOTSET)

    def json_of_response(self, response):
        """
        Decode json from response
        """

        return json.loads(response.data.decode("utf8"))

    def generic_put(self, url, a_dict):
        return self.client.put(url, data=json.dumps(a_dict), content_type="application/json", follow_redirects=True)

    def generic_post(self, url, a_dict):
        return self.client.post(url, data=json.dumps(a_dict), content_type="application/json", follow_redirects=True)

    def signup(self, a_dict):
        return self.client.post(
            url_for("auth.signup"), data=json.dumps(a_dict), content_type="application/json", follow_redirects=True
        )

    def login(self, a_dict):
        return self.client.post(
            url_for("auth.login"), data=json.dumps(a_dict), content_type="application/json", follow_redirects=True
        )

    def logout(self):
        return self.client.get(url_for("auth.logout"), follow_redirects=True)


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
    def test_signup_view(self):
        """
        Test that a sign up can be done
        """

        a_dict = dict(
            email="test@test.com",
            username="test",
            first_name="test",
            last_name="test",
            password="123456",
            is_admin=False,
        )
        response = self.signup(a_dict)
        self.assertEqual(response.status_code, 201)

    def test_login_OK_view(self):
        """
        Test that a login can be done with right credentials
        """

        a_dict = dict(email="non-admin@admin.com", password="123456")
        response = self.login(a_dict)
        self.assertEqual(response.status_code, 200)

    def test_login_FAIL_view(self):
        """
        Test that a login cannot be done with wrong credentials
        """

        a_dict = dict(email="non-admin@admin.com", password="654321")
        response = self.login(a_dict)
        self.assertEqual(response.status_code, 401)

    def test_logout_without_view(self):
        """
        Test that logout cannot be done without a login before
        """

        response = self.logout()
        self.assertEqual(response.status_code, 401)

    def test_logout_with_login_view(self):
        """
        Test that logout cannot be done without a login before
        """

        self.login(dict(email="non-admin@admin.com", password="123456"))
        response = self.logout()
        self.assertEqual(response.status_code, 200)

    def test_list_did_numbers_without_login_view(self):
        """
        Test list DID numbers without login (a redirection should be done)
        """

        target_url = url_for("user.list_didnumbers")
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_list_did_numbers_with_login_view(self):
        """
        Test list DID numbers with login
        """

        target_url = url_for("user.list_didnumbers")
        self.login(dict(email="non-admin@admin.com", password="123456"))
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_detail_did_numbers_without_login_view(self):
        """
        Test detail DID numbers without login (a redirection should be done)
        """

        target_url = url_for("user.didnumber_detail", id=1)
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_detail_did_numbers_with_login_view(self):
        """
        Test detail DID numbers with login
        """

        target_url = url_for("user.didnumber_detail", id=1)
        self.login(dict(email="non-admin@admin.com", password="123456"))
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_detail_did_number_that_does_not_exist_view(self):
        """
        Test detail DID number that does not exist
        """

        target_url = url_for("user.didnumber_detail", id=1000)
        self.login(dict(email="admin@admin.com", password="123456"))
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 404)

    def test_add_did_numbers_without_login_view(self):
        """
        Test add DID numbers without login (a redirection should be done)
        """

        target_url = url_for("user.add_didnumber")
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.post(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_add_did_numbers_with_login_view(self):
        """
        Test add DID numbers with login
        """

        target_url = url_for("user.add_didnumber")
        self.login(dict(email="non-admin@admin.com", password="123456"))
        a_dict = dict(
            value="+55 84 91234-0000",
            monthlyPrice="0.06",
            setupPrice="3.49",
            currency="U$",
        )
        response = self.generic_post(target_url, a_dict)
        self.assertEqual(response.status_code, 201)

    def test_add_did_number_that_already_exists_view(self):
        """
        Test add DID number that already exists
        """

        target_url = url_for("user.add_didnumber")
        self.login(dict(email="non-admin@admin.com", password="123456"))
        a_dict = dict(
            value="+55 84 91234-4320",
            monthlyPrice="0.06",
            setupPrice="3.49",
            currency="U$",
        )
        response = self.generic_post(target_url, a_dict)
        self.assertEqual(response.status_code, 403)

    def test_add_invalid_did_number_view(self):
        """
        Test add an invalid DID number
        """

        target_url = url_for("user.add_didnumber")
        self.login(dict(email="non-admin@admin.com", password="123456"))
        a_dict = dict(
            value=123456,
            monthlyPrice="0.06",
            setupPrice="3.49",
            currency="U$",
        )
        response = self.generic_post(target_url, a_dict)
        self.assertEqual(response.status_code, 500)

    def test_edit_did_numbers_without_login_view(self):
        """
        Test edit DID numbers without login (a redirection should be done)
        """

        target_url = url_for("user.edit_did_number", id=1)
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.put(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_edit_did_numbers_with_login_non_admin_view(self):
        """
        Test edit DID numbers with login but with no access permission (non-admin user)
        """

        target_url = url_for("user.edit_did_number", id=1)
        self.login(dict(email="non-admin@admin.com", password="123456"))
        a_dict = dict(
            value="+55 84 91234-0000",
            monthlyPrice="0.06",
            setupPrice="3.49",
            currency="U$",
        )
        response = self.generic_put(target_url, a_dict)
        self.assertEqual(response.status_code, 403)

    def test_edit_did_numbers_with_login_admin_view(self):
        """
        Test edit DID numbers with login and the user has access permission (is an admin user)
        """

        target_url = url_for("user.edit_did_number", id=1)
        self.login(dict(email="admin@admin.com", password="123456"))
        a_dict = dict(
            value="+55 84 91234-0000",
            monthlyPrice="0.06",
            setupPrice="3.49",
            currency="U$",
        )
        response = self.generic_put(target_url, a_dict)
        self.assertEqual(response.status_code, 200)

    def test_edit_did_number_that_does_not_exist_view(self):
        """
        Test edit DID number that does not exist
        """

        target_url = url_for("user.edit_did_number", id=1000)
        self.login(dict(email="admin@admin.com", password="123456"))
        response = self.client.put(target_url)
        self.assertEqual(response.status_code, 404)

    def test_edit_did_number_using_value_that_already_exist_view(self):
        """
        Test edit DID number using a value that already exist in the database
        """

        target_url = url_for("user.edit_did_number", id=1)
        a_dict = dict(
            value="+55 84 91234-4321",
            monthlyPrice="0.06",
            setupPrice="3.49",
            currency="U$",
        )
        self.login(dict(email="admin@admin.com", password="123456"))
        response = self.generic_put(target_url, a_dict)
        self.assertEqual(response.status_code, 500)

    def test_delete_did_numbers_without_login_view(self):
        """
        Test delete DID numbers without login (a redirection should be done)
        """

        target_url = url_for("user.delete_did_number", id=1)
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.delete(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_delete_did_numbers_with_login_non_admin_view(self):
        """
        Test delete DID numbers with login but with no access permission (non-admin user)
        """

        target_url = url_for("user.delete_did_number", id=1)
        self.login(dict(email="non-admin@admin.com", password="123456"))
        response = self.client.delete(target_url)
        self.assertEqual(response.status_code, 403)

    def test_delete_did_numbers_with_login_admin_view(self):
        """
        Test delete DID numbers with login and the user has access permission (is an admin user)
        """

        target_url = url_for("user.delete_did_number", id=1)
        self.login(dict(email="admin@admin.com", password="123456"))
        response = self.client.delete(target_url)
        self.assertEqual(response.status_code, 200)

    def test_delete_did_number_that_does_not_exist_view(self):
        """
        Test delete DID number that does not exist
        """

        target_url = url_for("user.delete_did_number", id=1000)
        self.login(dict(email="admin@admin.com", password="123456"))
        response = self.client.delete(target_url)
        self.assertEqual(response.status_code, 404)

    def test_list_employees_without_login_view(self):
        """
        Test list employees without login (a redirection should be done)
        """

        target_url = url_for("user.list_employees")
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_list_employees_with_login_non_admin_view(self):
        """
        Test list employees with login but with no access permission (non-admin user)
        """

        target_url = url_for("user.list_employees")
        self.login(dict(email="non-admin@admin.com", password="123456"))
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 403)

    def test_list_employees_with_login_admin_view(self):
        """
        Test list employees with login and the user has access permission (is an admin user)
        """

        target_url = url_for("user.list_employees")
        self.login(dict(email="admin@admin.com", password="123456"))
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_employees_details_without_login_view(self):
        """
        Test list employees details without login (a redirection should be done)
        """

        target_url = url_for("user.list_employees", id=1)
        redirect_url = url_for("auth.login", next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_employees_details_with_login_non_admin_view(self):
        """
        Test list employees details with login but with no access permission (non-admin user)
        """

        target_url = url_for("user.list_employees", id=1)
        self.login(dict(email="non-admin@admin.com", password="123456"))
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 403)

    def test_employees_details_with_login_admin_view(self):
        """
        Test list employees_details with login and the user has access permission (is an admin user)
        """

        target_url = url_for("user.list_employees", id=1)
        self.login(dict(email="admin@admin.com", password="123456"))
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_employee_detail_does_not_exist_view(self):
        """
        Test list employee detail whose doesn't exist
        """

        target_url = url_for("user.employee_detail", id=1000)
        self.login(dict(email="admin@admin.com", password="123456"))
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 404)


class TestErrorHandlings(TestBase):
    def test_400_bad_request(self):
        """
        Create route to abort the request with the 400 Bad Request
        """

        @self.app.route("/400")
        def bad_request():
            abort(400)

        response = self.client.get("/400")
        self.assertEqual(response.status_code, 400)
        self.assertTrue("400 Bad Request" in str(response.data))

    def test_401_unauthorized(self):
        """
        Create route to abort the request with the 4001 Unauthorized
        """

        @self.app.route("/401")
        def unauthorized():
            abort(401)

        response = self.client.get("/401")
        self.assertEqual(response.status_code, 401)
        self.assertTrue("401 Unauthorized" in str(response.data))

    def test_403_forbidden(self):
        """
        Create route to abort the request with the 403 Forbidden
        """

        @self.app.route("/403")
        def forbidden_error():
            abort(403)

        response = self.client.get("/403")
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Forbidden" in str(response.data))

    def test_404_not_found(self):
        """
        Access a page that does not exist
        """

        response = self.client.get("/notexistpage")
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Not Found" in str(response.data))

    def test_405_not_found(self):
        """
        Access a page that does not exist
        """

        @self.app.route("/405", methods=["DELETE"])
        def method_not_allowed():
            pass

        response = self.client.get("/405")
        self.assertEqual(response.status_code, 405)
        self.assertTrue("405 Method Not Allowed" in str(response.data))

    def test_500_internal_server_error(self):
        """
        Create route to abort the request with the 500 Error
        """

        @self.app.route("/500")
        def internal_server_error():
            abort(500)

        response = self.client.get("/500")
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Internal Server Error" in str(response.data))


if __name__ == "__main__":
    unittest.main()
