from flask import redirect

from tests.conftest import get_url


def test_list_employees_without_login_view(app, client):
    """
    Test list employees without login (a redirection should be done)
    """

    target_url = get_url(app=app, url="user.list_employees")
    redirect_url = redirect(get_url(app=app, url="auth.login", next_url=target_url))
    response = client.get(target_url)
    assert response.status_code == 302
    assert redirect_url.data == response.data


def test_list_employees_with_login_non_admin_view(app, auth, client):
    """
    Test list employees with login but with no access permission (non-admin user)
    """

    target_url = get_url(app=app, url="user.list_employees")
    auth.login(a_dict=dict(email="non-admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 403
    assert b"The current user is not an admin" in response.data


def test_list_employees_with_login_admin_view(app, auth, client):
    """
    Test list employees with login and the user has access permission (is an admin user)
    """

    target_url = get_url(app=app, url="user.list_employees")
    auth.login(a_dict=dict(email="admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_employees_details_without_login_view(app, client):
    """
    Test list employees details without login (a redirection should be done)
    """

    target_url = get_url(app=app, url="user.list_employees", id=1)
    redirect_url = redirect(get_url(app=app, url="auth.login", next_url=target_url))
    response = client.get(target_url)
    assert response.status_code == 302
    assert response, redirect_url


def test_employees_details_with_login_non_admin_view(app, auth, client):
    """
    Test list employees details with login but with no access permission (non-admin user)
    """

    target_url = get_url(app=app, url="user.list_employees", id=1)
    auth.login(a_dict=dict(email="non-admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 403
    assert b"The current user is not an admin" in response.data


def test_employees_details_with_login_admin_view(app, auth, client):
    """
    Test list employees_details with login and the user has access permission (is an admin user)
    """

    target_url = get_url(app=app, url="user.list_employees", id=1)
    auth.login(a_dict=dict(email="admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_employee_detail_does_not_exist_view(app, auth, client):
    """
    Test list employee detail whose doesn't exist
    """

    target_url = get_url(app=app, url="user.employee_detail", id=10000000)
    auth.login(a_dict=dict(email="admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 404
