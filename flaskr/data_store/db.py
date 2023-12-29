import sqlite3
import psycopg
from psycopg.rows import dict_row

import os
import random
import string


import click
from flask import current_app, g


def get_db(conn_type="read"):
    if "db" not in g:
        if conn_type == "read":
            g.db_read = psycopg.connect(
                dbname=os.environ["READ_DB_NAME"],
                user=os.environ["READ_DB_USER"],
                password=os.environ["READ_DB_PASS"],
                host=os.environ["DB_HOST"],
                port=os.environ["DB_PORT"],
                sslmode=os.environ["DB_SSL_MODE"],
                row_factory=dict_row,
            )
            return g.db_read
        elif conn_type == "write":
            g.db_write = psycopg.connect(
                dbname=os.environ["WRITE_DB_NAME"],
                user=os.environ["WRITE_DB_USER"],
                password=os.environ["WRITE_DB_PASS"],
                host=os.environ["DB_HOST"],
                port=os.environ["DB_PORT"],
                sslmode=os.environ["DB_SSL_MODE"],
                row_factory=dict_row,
            )
            return g.db_write
        else:
            return None


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
        print(code)


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
