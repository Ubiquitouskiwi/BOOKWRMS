import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .data_store import db

    db.init_app(app)

    from .pages import auth

    app.register_blueprint(auth.bp)

    from .pages import home

    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint="index")

    # from .pages import scanner
    # app.register_blueprint(scanner.bp)

    app.app_context().push()

    return app
