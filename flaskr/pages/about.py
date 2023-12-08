import functools
import bcrypt
import json
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    send_from_directory,
    app,
    jsonify,
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.data_store.db import get_db

bp = Blueprint("about", __name__)


@bp.route("/about", methods=["GET"])
def index():
    return render_template("about/index.html")


@bp.route("/about/generate_db_file")
def generate_file():
    db = get_db()
    authors = db.execute("SELECT * FROM author").fetchall()
    books = db.execute("SELECT * FROM book").fetchall()
    checkouts = db.execute("SELECT * FROM checkout_log").fetchall()
    logins = db.execute("SELECT * FROM login").fetchall()
    users = db.execute("SELECT * FROM user").fetchall()
    invite_codes = db.execute("SELECT * FROM invite_code").fetchall()

    data = {"author": [], "book": [], "checkout_log": [], "login": [], "user": []}
    for item in authors:
        row = []
        for index, key in enumerate(item):
            row.append(str(key))
        data["author"].append(str(row).replace("[", "(").replace("]", ")"))

    for item in books:
        row = []
        for key in item:
            row.append(str(key))
        data["book"].append(str(row).replace("[", "(").replace("]", ")"))

    for item in checkouts:
        row = []
        for key in item:
            row.append(str(key))
        data["checkout_log"].append(str(row).replace("[", "(").replace("]", ")"))

    for item in logins:
        row = []
        for key in item:
            row.append(str(key))
        data["login"].append(str(row).replace("[", "(").replace("]", ")"))

    for item in users:
        row = []
        for key in item:
            row.append(str(key))
        data["user"].append(str(row).replace("[", "(").replace("]", ")"))

    for item in invite_codes:
        row = []
        for key in item:
            row.append(str(key))
        data["invite_code"].append(str(row).replace("[", "(").replace("]", ")"))
    print(data)

    return jsonify(data)

    return render_template("about/index.html")


@bp.route("/about/insert_data", methods=["POST", "GET"])
def insert_db():
    if request.method == "POST":
        json_string = request.form["db_json"]
        db_data = json.loads(json_string)
        db = get_db()

        for value in db_data["login"]:
            sql = (
                "INSERT INTO login (email, password, created_at, deleted) VALUES "
                + "("
                + ",".join(value.split(", ")[1:])
            )
            print(sql)
            db.execute(sql)
            db.commit()

        for value in db_data["user"]:
            sql = (
                "INSERT INTO user (first_name, last_name, email, is_admin, created_at, deleted) VALUES "
                + "("
                + ",".join(value.split(", ")[1:])
            )
            print(sql)
            db.execute(sql)
            db.commit()

        for value in db_data["author"]:
            sql = (
                "INSERT INTO author (first_name, last_name, middle_name, olid, created_at, deleted) VALUES "
                + "("
                + ",".join(value.split(", ")[1:])
            )
            print(sql)
            db.execute(sql)
            db.commit()

        for value in db_data["book"]:
            sql = (
                "INSERT INTO book (title, author_id, isbn, illustration_url, olid, created_at, deleted) VALUES "
                + "("
                + ",".join(value.split(", ")[1:])
            )
            print(sql)
            db.execute(sql)
            db.commit()

        for value in db_data["checkout_log"]:
            sql = (
                "INSERT INTO checkout_log (book_id, patron_name, checkout_date, checkout_duration, checkin_date, renew_count, returned, created_at, deleted) VALUES "
                + "("
                + ",".join(value.split(", ")[1:])
            )
            print(sql)
            db.execute(sql)
            db.commit()

    return render_template("about/insert_db.html")
