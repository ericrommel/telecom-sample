import os

from flask import Flask, jsonify
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from log import Log

log = Log("evolux-project").get_logger(logger_name="app")


db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()


def create_app(config_name=None):
    log.info(f"Create app (config_name: {config_name})")
    if os.getenv("FLASK_CONFIG") == "production":
        app = Flask(__name__)
        log.info(f"Get configs from {os.getenv('FLASK_CONFIG')}")
        app.config.update(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS"),
        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        log.info(f"Get configs from {os.getenv('FLASK_CONFIG')}")
        if config_name is None:
            log.info("Load the instance config, if it exists, when not testing")
            app.config.from_pyfile("config.py")
        else:
            log.info(f"Load the config name: {config_name}")
            app.config.from_mapping(config_name)

    # ensure the instance folder exists
    try:
        log.info("Create instance folder")
        os.makedirs(app.instance_path)
    except OSError as e:
        log.error(f"Error: {e}")
        pass

    log.info("Initialize the application for the use with its setup DB")
    db.init_app(app)

    log.info("Register and attach the `LoginManager`")
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page"
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    from app import models

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .user import user as user_blueprint

    app.register_blueprint(user_blueprint)

    # Errors
    @app.errorhandler(400)
    def bad_request(e):
        log.error(e)
        return jsonify(error=str(e)), 400

    # Errors
    @app.errorhandler(401)
    def unauthorized(e):
        log.error(e)
        return jsonify(error=str(e)), 401

    @app.errorhandler(403)
    def forbidden(e):
        log.error(e)
        return jsonify(error=str(e)), 403

    @app.errorhandler(404)
    def page_not_found(e):
        log.error(e)
        return jsonify(error=str(e)), 404

    @app.errorhandler(405)
    def not_logged(e):
        log.error(e)
        return jsonify(error=str(e)), 405

    @app.errorhandler(500)
    def internal_server_error(e):
        log.error(e)
        return jsonify(error=str(e)), 500

    return app
