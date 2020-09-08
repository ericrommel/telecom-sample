Project Sample
======

A project sample app built in Flask/SQLAlchemy.

Install
-------

The default Git version is the master branch. ::

    # clone the repository
    $ git clone git@github.com:ericrommel/telecom-sample.git


This project is using pipenv as a packaging tool. Learn more about pipenv here (<https://realpython.com/pipenv-guide/>)::

    $ pip install pipenv
    $ pipenv sync -d

It will install all requirements needed.


Run
---

Set the environment variables::

    $ export FLASK_CONFIG=development
    $ export FLASK_APP=run.py
    $ flask init-db
    $ flask run

Or on Windows cmd::

    > set FLASK_CONFIG=development
    > set FLASK_APP=run.py
    > flask init-db
    > flask run

Open http://127.0.0.1:5000 in a browser.


Tests
----

From Postman::
- Import the collection file: postman/Evolux.postman_collection.json
- Import the environment file: postman/env_evolux.postman_environment.json

From Python code tests (unit tests)::

    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser