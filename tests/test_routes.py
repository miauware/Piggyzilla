import pytest
from werkzeug.security import generate_password_hash


def test_home_redirect_authenticated(client):
    """Tests if the home page redirects to the dashboard when authenticated"""
    # INFO: Simulate an authenticated user
    with client.application.test_request_context():
        from flask_login import login_user
        from models.user import User

        # INFO: Create a test user
        user = User(username="test", password=generate_password_hash("password"))
        from extensions import db

        db.session.add(user)
        db.session.commit()
        login_user(user)

    response = client.get("/")
    assert response.status_code == 302
    assert "dashboard" in response.headers["Location"]


def test_home_render_template_unauthenticated(client):
    """NOTE: Tests if the home page renders the template when not authenticated"""
    response = client.get("/")
    assert response.status_code == 200
    # INFO: Verify if it contains elements from the index.html template
    assert b"Login" in response.data


def test_set_language(client):
    """Tests language change"""
    response = client.post("/set_language/pt")
    assert response.status_code == 302
    # NOTE: Verify if the session was updated
    with client:
        with client.session_transaction() as sess:
            assert sess.get("lang") == "pt"
