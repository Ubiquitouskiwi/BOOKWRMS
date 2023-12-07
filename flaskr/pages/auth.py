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

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", [user_id]).fetchone()
        )


@bp.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["confirm_password"]
        invite_code = request.form["invite_code"]
        db = get_db()

        if not first_name:
            error = "First name is required."
        elif not last_name:
            error = "Last name is required."
        elif not email:
            error = "All users must have an email"
        elif not password or not password_confirm:
            error = "Password can't be blank"
        elif password != password_confirm:
            error = "Passwords must match."
        elif not invite_code:
            error = "Must have invite code to register."

        if error is None:
            invite_code_id = db.execute(
                "SELECT id FROM invite_code WHERE code = ? AND valid = ? AND deleted = ?",
                [invite_code, True, False],
            ).fetchone()["id"]
            if invite_code_id is not None:
                hashed_pass = hash_password(password)
                try:
                    db.execute(
                        "INSERT INTO login (email, password) VALUES (?, ?)",
                        (email, hashed_pass),
                    )
                    db.commit()
                    db.execute(
                        "INSERT INTO user (first_name, last_name, email, is_admin) values (?, ?, ?, ?)",
                        (first_name.lower(), last_name.lower(), email, True),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"{first_name} {last_name} is already registered"
                    db.execute(
                        "UPDATE invite_code SET valid = FALSE, user_email = ? WHERE id = ?",
                        [email, invite_code_id],
                    )
                    db.commit()
                else:
                    return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        plain_text_password = request.form["password"]
        db = get_db()
        error = None

        if not email:
            error = "Must provide email"
        if not plain_text_password:
            error = "Must provide password"

        if error is None:
            login_account_pass = db.execute(
                "SELECT password FROM login WHERE email = ?", (email,)
            ).fetchone()
            if login_account_pass:
                if check_password(plain_text_password, login_account_pass["password"]):
                    user_account_id = db.execute(
                        "SELECT id FROM user WHERE email = ?", (email,)
                    ).fetchone()
                    session.clear()
                    session["user_id"] = user_account_id["id"]
                    return redirect(url_for("index"))
                else:
                    error = "Incorrect login credentials"
            else:
                error = "Incorrect login credentials"
        flash(error)
    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def hash_password(plain_text_password):
    # Salt is saved into hash
    return bcrypt.hashpw(plain_text_password.encode("utf8"), bcrypt.gensalt())


def check_password(plain_text_password, hashed_pass):
    # Salt value was saved into hash itself
    return bcrypt.checkpw(plain_text_password.encode("utf8"), hashed_pass)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
