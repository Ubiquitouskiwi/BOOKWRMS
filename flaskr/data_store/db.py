import sqlite3

import os
import random
import string


import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("data_store/schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

    for i in range(10):
        int_code = str(random.randint(0, 9999))
        alpha_code = "".join(random.choices(string.ascii_uppercase, k=2))
        code = "".join([alpha_code, int_code])
        db.execute("INSERT INTO invite_code (code) VALUES (?)", [code])
        db.commit()


@click.command("init-db")
@click.option("--dev", default=False)
def init_db_command(dev):
    init_db()
    click.echo("Initialized the database.")

    if dev:
        db = get_db()
        with current_app.open_resource("data_store/dev_data.sql") as f:
            db.executescript(f.read().decode("utf8"))


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
