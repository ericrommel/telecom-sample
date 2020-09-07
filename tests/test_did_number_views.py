import json

from flask import redirect
from tests.conftest import get_url


def test_list_did_numbers_without_login_view(app, client):
    """
    Test list DID numbers without login (a redirection should be done)
    """

    target_url = get_url(app=app, url="user.list_didnumbers")
    redirect_url = redirect(get_url(app=app, url="auth.login", next_url=target_url))
    response = client.get(target_url)
    assert response.status_code == 302
    assert redirect_url.data == response.data


def test_list_did_numbers_with_login_view(app, auth, client):
    """
    Test list DID numbers with login
    """

    target_url = get_url(app=app, url="user.list_didnumbers")
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_detail_did_numbers_without_login_view(app, client):
    """
    Test detail DID numbers without login (a redirection should be done)
    """

    target_url = get_url(app=app, url="user.didnumber_detail", id=1)
    redirect_url = redirect(get_url(app=app, url="auth.login", next_url=target_url))
    response = client.get(target_url)
    assert response.status_code == 302
    assert redirect_url.data == response.data


def test_detail_did_numbers_with_login_view(app, auth, client):
    """
    Test detail DID numbers with login
    """

    target_url = get_url(app=app, url="user.didnumber_detail", id=1)
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_detail_did_number_that_does_not_exist_view(app, auth, client):
    """
    Test detail DID number that does not exist
    """

    target_url = get_url(app=app, url="user.didnumber_detail", id=1000000)
    auth.login(dict(email="admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 404


def test_add_did_numbers_without_login_view(app, client):
    """
    Test add DID numbers without login (a redirection should be done)
    """

    target_url = get_url(app=app, url="user.add_didnumber")
    redirect_url = redirect(get_url(app=app, url="auth.login", next_url=target_url))
    response = client.post(target_url)
    assert response.status_code == 302
    assert redirect_url.data == response.data


def test_add_did_numbers_with_login_view(app, auth, client):
    """
    Test add DID numbers with login
    """

    target_url = get_url(app=app, url="user.add_didnumber")
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    a_dict = dict(
        value="+55 84 91234-0000",
        monthlyPrice="0.06",
        setupPrice="3.49",
        currency="U$",
    )
    response = auth.generic_post(target_url, a_dict)
    print(response)
    assert response.status_code == 201


def test_add_did_number_that_already_exists_view(app, auth, client):
    """
    Test add DID number that already exists
    """

    target_url = get_url(app=app, url="user.add_didnumber")
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    a_dict = dict(
        value="+55 84 91234-4320",
        monthlyPrice="0.06",
        setupPrice="3.49",
        currency="U$",
    )
    response = auth.generic_post(target_url, a_dict)
    assert response.status_code == 403


#
# def test_add_invalid_did_number_view(app, auth, client):
#     """
#     Test add an invalid DID number
#     """
#
#     target_url = get_url(app=app, url="user.add_didnumber")
#     auth.login(dict(email="non-admin@admin.com", password="123456"))
#     a_dict = dict(
#         value=123456,
#         monthlyPrice="0.06",
#         setupPrice="3.49",
#         currency="U$",
#     )
#     response = auth.generic_post(target_url, a_dict)
#     assert response.status_code == 500


def test_edit_did_numbers_without_login_view(app, auth, client):
    """
    Test edit DID numbers without login (a redirection should be done)
    """

    target_url = get_url(app=app, url="user.edit_did_number", id=1)
    redirect_url = redirect(get_url(app=app, url="auth.login", next_url=target_url))
    response = client.put(target_url)
    assert response.status_code == 302
    assert redirect_url.data == response.data


def test_edit_did_numbers_with_login_non_admin_view(app, auth, client):
    """
    Test edit DID numbers with login but with no access permission (non-admin user)
    """

    target_url = get_url(app=app, url="user.edit_did_number", id=1)
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    a_dict = dict(
        value="+55 84 91234-0000",
        monthlyPrice="0.06",
        setupPrice="3.49",
        currency="U$",
    )
    response = auth.generic_put(target_url, a_dict)
    assert response.status_code == 403


def test_edit_did_numbers_with_login_admin_view(app, auth, client):
    """
    Test edit DID numbers with login and the user has access permission (is an admin user)
    """

    target_url = get_url(app=app, url="user.edit_did_number", id=1)
    auth.login(dict(email="admin@admin.com", password="123456"))
    a_dict = dict(
        value="+55 84 91234-0000",
        monthlyPrice="0.06",
        setupPrice="3.49",
        currency="U$",
    )
    response = auth.generic_put(target_url, a_dict)
    assert response.status_code == 200


def test_edit_did_number_that_does_not_exist_view(app, auth, client):
    """
    Test edit DID number that does not exist
    """

    target_url = get_url(app=app, url="user.edit_did_number", id=1000)
    auth.login(dict(email="admin@admin.com", password="123456"))
    response = client.put(target_url)
    assert response.status_code == 404


def test_edit_did_number_using_value_that_already_exist_view(app, auth, client):
    """
    Test edit DID number using a value that already exist in the database
    """

    target_url = get_url(app=app, url="user.edit_did_number", id=1)
    a_dict = dict(
        value="+55 84 91234-4321",
        monthlyPrice="0.06",
        setupPrice="3.49",
        currency="U$",
    )
    auth.login(dict(email="admin@admin.com", password="123456"))
    response = auth.generic_put(target_url, a_dict)
    assert response.status_code == 400


def test_delete_did_numbers_without_login_view(app, auth, client):
    """
    Test delete DID numbers without login (a redirection should be done)
    """

    target_url = get_url(app=app, url="user.delete_did_number", id=1)
    redirect_url = redirect(get_url(app=app, url="auth.login", next_url=target_url))
    response = client.delete(target_url)
    assert response.status_code == 302
    assert redirect_url.data == response.data


def test_delete_did_numbers_with_login_non_admin_view(app, auth, client):
    """
    Test delete DID numbers with login but with no access permission (non-admin user)
    """

    target_url = get_url(app=app, url="user.delete_did_number", id=1)
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    response = client.delete(target_url)
    assert response.status_code == 403


def test_delete_did_numbers_with_login_admin_view(app, auth, client):
    """
    Test delete DID numbers with login and the user has access permission (is an admin user)
    """

    target_url = get_url(app=app, url="user.delete_did_number", id=1)
    auth.login(dict(email="admin@admin.com", password="123456"))
    response = client.delete(target_url)
    assert response.status_code == 200


def test_delete_did_number_that_does_not_exist_view(app, auth, client):
    """
    Test delete DID number that does not exist
    """

    target_url = get_url(app=app, url="user.delete_did_number", id=1000)
    auth.login(dict(email="admin@admin.com", password="123456"))
    response = client.delete(target_url)
    assert response.status_code == 404
