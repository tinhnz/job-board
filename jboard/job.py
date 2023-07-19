from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from jboard.auth import login_required
from jboard.db import get_db

bp = Blueprint("job", __name__)


def get_job(id):
    """Get a job and its author by id.

    :param id: id of job to get
    :return: the job with author information
    :raise 404: if a job with the given id doesn't exist
    """
    db = get_db()
    db.execute(
        "SELECT id, company, salary, title, body, created_at FROM jobs WHERE id = %s",
        (id,),
    )
    job = db.fetchone()

    if job is None:
        abort(404, f"Post id {id} doesn't exist.")

    return job


@bp.route("/")
@login_required
def home():
    """Show all the posts, most recent first."""
    db = get_db()
    db.execute(
        "SELECT j.id, company, salary, title, body, created_at, username as author "
        "FROM jobs j JOIN users u ON j.author_id = u.id "
        "ORDER BY created_at DESC",
    )
    jobs = db.fetchall()
    return render_template("job/view.html", jobs=jobs)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a job if the current user is the editor."""
    if g.user["role"] != 'editor':
        abort(403)

    if request.method == "POST":
        print(request.form)
        title = request.form["title"]
        body = request.form["description"]
        company = request.form["company"]
        salary = request.form["salary"]
        db = get_db()
        db.execute(
            "INSERT INTO jobs (title, body, company, salary, author_id) VALUES (%s, %s, %s, %s, %s)",
            (title, body, company, salary, g.user["id"]),
        )
        return redirect(url_for("job.home"))

    return render_template("job/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a job if the current user is the editor."""
    if g.user["role"] != 'editor':
        abort(403)
    
    job = get_job(id)
    if request.method == "POST":
        print(request.form)
        title = request.form["title"]
        body = request.form["description"]
        company = request.form["company"]
        salary = request.form["salary"]

        db = get_db()
        db.execute(
            "UPDATE jobs SET title = %s, body = %s, company = %s, salary = %s WHERE id = %s",
            (title, body, company, salary, id),
        )
        return redirect(url_for("job.home"))

    return render_template("job/update.html", job=job)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a job.

    Ensures that the job exists and that the logged in user is the editor.
    """
    if g.user["role"] != 'editor':
        abort(403)

    get_job(id)
    db = get_db()
    db.execute("DELETE FROM jobs WHERE id = %s", (id,))
    return redirect(url_for("job.home"))
