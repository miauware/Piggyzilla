from flask import Blueprint, request, jsonify, render_template_string, render_template
from flask_login import login_required
from main import db, csrf

bp = Blueprint("api", __name__)


@bp.route("/api/csrf-token", methods=["GET"])
@login_required
def get_csrf_token():
    csrf_token = request.cookies.get("csrf_token")
    if not csrf_token:
        csrf_token_html = render_template_string("{{ csrf_token() }}")
        response = jsonify({"csrf_token": csrf_token_html})
        response.set_cookie("csrf_token", csrf_token_html)
    else:
        response = jsonify({"csrf_token": csrf_token})
    return response
