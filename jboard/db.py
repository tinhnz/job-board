import psycopg2
from psycopg2.extras import RealDictCursor

import click
from flask import current_app
from flask import g


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db_conn" not in g:
        g.db_conn = psycopg2.connect(
            current_app.config["DATABASE_URI"],
            cursor_factory=RealDictCursor,
        )
        g.db_conn.autocommit = True
        g.db_cursor = g.db_conn.cursor()

    return g.db_cursor


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db_cursor = g.pop("db_cursor", None)

    if db_cursor is not None:
        db_cursor.close()

    db_conn = g.pop("db_conn", None)

    if db_conn is not None:
        db_conn.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("scripts/ddl.sql") as f:
        # Open a cursor to perform database operations
        db.execute(f.read().decode("utf8"))

    with current_app.open_resource("scripts/dml.sql") as f:
        # Open a cursor to perform database operations
        db.execute(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
