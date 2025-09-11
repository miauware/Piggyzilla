from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    make_response,
    jsonify,
    render_template,
)
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash
from models.user import User
from main import db, csrf
from datetime import datetime, timedelta
import secrets
from functools import wraps

bp = Blueprint("auth", __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated:
            return f(*args, **kwargs)

        token = request.cookies.get("session_token")
        if token:
            user = User.query.filter_by(session_token=token).first()
            if user and user.session_expiration and user.session_expiration > datetime.utcnow():
                login_user(user, remember=False)
                return f(*args, **kwargs)
            else:
                if user:
                    user.session_token = None
                    user.session_expiration = None
                    db.session.commit()

        return redirect(url_for("auth.auth"))

    return decorated


@bp.route("/auth", methods=["GET", "POST"])
@csrf.exempt
def auth():
    if current_user.is_authenticated:
        return redirect(url_for("index.home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=False)

            resp = make_response(jsonify({"success": True}), 200)

            if remember:
                token = secrets.token_urlsafe(32)
                user.session_token = token
                user.session_expiration = datetime.utcnow() + timedelta(days=30)
                db.session.commit()

                resp.set_cookie(
                    "session_token",
                    token,
                    max_age=30*24*3600,
                    httponly=True,
                    samesite="Lax",
                )
            else:
                user.session_token = None
                user.session_expiration = None
                db.session.commit()
                if request.cookies.get("session_token"):
                    resp.set_cookie("session_token", "", expires=0)

            return resp
        else:
            return make_response(jsonify({"success": False}), 200)

    return render_template("index.html")


@bp.route("/logout")
@login_required
def logout():
    user = current_user
    user.session_token = None
    user.session_expiration = None
    db.session.commit()

    logout_user()
    resp = redirect(url_for("index.home"))
    resp.set_cookie("session_token", "", expires=0)
    return resp
