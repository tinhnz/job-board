import functools
import psycopg2

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from jboard.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.signin"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        db.execute("SELECT id, username, role FROM users WHERE id = %s", [user_id])
        g.user = db.fetchone()


@bp.route("/signup", methods=("GET", "POST"))
def signup():
    """Sign up a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db = get_db()
                db.execute(
                    "INSERT INTO users (username, password, role) VALUES (%s, %s, 'viewer')",
                    (username, generate_password_hash(password)),
                )
            except psycopg2.IntegrityError as e:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.signin"))

        flash(error)

    return render_template("auth/signup.html")


@bp.route("/signin", methods=("GET", "POST"))
def signin():
    """Sign in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        db.execute("SELECT * FROM users WHERE username = %s", [username])
        user = db.fetchone()

        error = None
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            session["user_role"] = user["role"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/signin.html")


@bp.route("/signout")
def signout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
