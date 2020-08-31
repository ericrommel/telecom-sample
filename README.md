Flask (https://github.com/pallets/flask) — my favorite Python web framework. It’s small, minimal, and simple.
Flask-SQLAlchemy (https://github.com/mitsuhiko/flask-sqlalchemy)— an extremely popular ORM for Flask. It allows you to interact with relational database servers like Postgres, MySQL, SQLite, etc. In this tutorial, we’ll be using SQLite as our database, but any of the others would work equally well with no code changes.
Flask-OIDC (https://github.com/puiterwijk/flask-oidc) — an OpenID Connect library for Flask. OpenID Connect is an open protocol that handles user authentication and authorization. It’s the “modern” way to handle authentication on the web.
Okta (https://developer.okta.com/) — a free-to-use API service that acts as an OpenID Connect authorization server. Okta will store user accounts for your app and make it possible to handle user registration, login, etc. in a simple way.
python-slugify (https://github.com/un33k/python-slugify) — a simple Python library that generates web-friendly URLs. We’ll use this to convert blog post titles into URLs that look nice.

Org URL:https://dev-753668.okta.com
Client ID: 0oat35665AdvRAiGl4x6
Client Secret: uK0ozg4NnPNl57SoEOaFFcmcBvfk09e6tX3K6Oz_
Token Value: 00rMSK4xvQkVdoAk-756OjfOCept2sLUD_lM5nzlAB

set FLASK_CONFIG=development
set FLASK_APP=run.py
flask run

1. Add a ADMIN user:
   admin = Employee(
        email="admin@admin.com",
        username="admin",
        password="123456",
        is_admin=True
   )