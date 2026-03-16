from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    make_response,
    jsonify,
    render_template,
    Response,
    current_app,
    session,
)
from flask_babel import _
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from models.user import User
from main import db, csrf

bp = Blueprint("index", __name__)


@csrf.exempt
@bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    return render_template("index.html")


@bp.route('/set_language/<language>', methods=['POST'])
def set_language(language):
    session['lang'] = language
    next_page = request.referrer or url_for('index.home')
    return redirect(next_page)

@bp.route('/static/css/custom-colors.css')
def customcss():
    customfg = "#1f2936"
    customfg2 = "#5e00d1"
    custombg = " radial-gradient(circle, #8b3cff, #4f26e5);"
    custombutton = "#334155"
    textcolor = "#ffffff"
    customfont = "Brush Script MT,cursive"
    css = f"""
    :root {{
        --customfg: {customfg};
        --customfg2: {customfg2};
        --custombg: {custombg};
        --custombutton: {custombutton};
        --textcolor: {textcolor};
        --customfont: {customfont};
    }}
    .custombg {{
        background: var(--custombg);
    }}
    .customfg {{
        background-color: var(--customfg);
    }}
    .customfg2 {{
        background-color: var(--customfg2);
    }}
    .custombutton {{
        background-color: var(--custombutton);
    }}
    .customtext {{
        color: var(--textcolor);
        font-family: var(--customfont);
    }}
    """
    return Response(css, mimetype='text/css')
