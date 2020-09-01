1. Set environment variables for FLASK
set FLASK_CONFIG=development
set FLASK_APP=run.py

flask db init
flask db migrate
flask db upgrade
flask run

1. Add a ADMIN user:
   admin = Employee(
        email="admin@admin.com",
        username="admin",
        password="123456",
        is_admin=True
   )