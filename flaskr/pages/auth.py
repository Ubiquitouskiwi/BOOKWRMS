import functools
from argon2 import PasswordHasher
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
from psycopg import IntegrityError

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        db_cursor = db.cursor()
        results = db_cursor.execute("SELECT * FROM account WHERE id = %s", [user_id])
        g.user = db_cursor.fetchone()


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
        write_db = get_db("write")
        read_db = get_db("read")

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
            db_read_cursor = read_db.cursor()
            db_read_cursor.execute(
                "SELECT id FROM invite_code WHERE code = %s AND used = %s AND deleted = %s",
                [invite_code, False, False],
            )
            invite_code_id = db_read_cursor.fetchone()["id"]
            if invite_code_id is not None:
                hashed_pass = hash_password(password)
                db_write_cursor = write_db.cursor()
                try:
                    db_write_cursor.execute(
                        "INSERT INTO login (email, pass) VALUES (%s, %s)",
                        (email, hashed_pass.decode("utf8")),
                    )
                    db_write_cursor.execute(
                        "INSERT INTO account (first_name, last_name, email, is_admin) values (%s, %s, %s, %s)",
                        (first_name.lower(), last_name.lower(), email, True),
                    )
                    db_write_cursor.execute(
                        "UPDATE invite_code SET used = TRUE, user_email = %s, used_date = CURRENT_TIMESTAMP WHERE id = %s",
                        [email, invite_code_id],
                    )
                    write_db.commit()
                    db_write_cursor.close()
                    db_read_cursor.close()

                    return redirect(url_for("auth.login"))
                except IntegrityError:
                    error = f"{first_name} {last_name} is already registered"
        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        plain_text_password = request.form["password"]
        read_db = get_db("read")
        error = None

        if not email:
            error = "Must provide email"
        if not plain_text_password:
            error = "Must provide password"

        if error is None:
            db_read_cursor = read_db.cursor()
            db_read_cursor.execute("SELECT pass FROM login WHERE email = %s", [email])
            login_account_pass = db_read_cursor.fetchone()
            if login_account_pass:
                "DO BCRYPT FLOW THEN SAVE ARGON PASS"
                if check_password(plain_text_password, login_account_pass["pass"]):
                    db_read_cursor.execute(
                        "SELECT id FROM account WHERE email = %s", [email]
                    )
                    user_account_id = db_read_cursor.fetchone()
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
    isMatch = False
    if hashed_pass[:1] == "$2":
        isMatch = bcrypt.checkpw(
            plain_text_password.encode("utf8"), hashed_pass.encode("utf8")
        )
    else:
        passHasher = PasswordHasher()
        isMatch = passHasher.verify(hashed_pass, plain_text_password)
    return isMatch


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

    # TODO: create db read and db write connect and switch between them
