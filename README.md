## Steps to execute

1. Set Flask environment variables
- FLASK_CONFIG=development
- FLASK_APP=run.py

2. Database
- The flask app is using instance folder. Here an example of the config.py<br>
<code>
SECRET_KEY = "oSyv7P4vciF5R17raC1+ew=="
project_dir = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(project_dir, "telecom-prod.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # avoid FSADeprecationWarning

- After that, initialize, migrate and upgrade<br>
<code>
flask db migrate<br>
flask db upgrade<br>
flask run<br>

3. Run the app
- flask run