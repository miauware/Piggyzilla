import pytest
import os
import sys

# INFO: Add the root directory to the path to import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import app as flask_app


@pytest.fixture
def app():
    # CONFIG: Configure app for tests
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["WTF_CSRF_ENABLED"] = False  # CONFIG: Disable CSRF for testing

    with flask_app.app_context():
        from extensions import db

        db.create_all()

    yield flask_app

    # INFO: Cleanup after tests
    with flask_app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
