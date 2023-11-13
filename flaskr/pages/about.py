import functools
import bcrypt
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.data_store.db import get_db

bp = Blueprint("about", __name__)


@bp.route("/about", methods=["GET"])
def index():
    return render_template("about/index.html")
