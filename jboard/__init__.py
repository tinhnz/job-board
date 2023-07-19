import os

from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if 'GOOGLE_CLOUD_PROJECT' in os.environ:
        # GCP
        print("Loading config.gcp")
        app.config.from_object('jboard.config.gcp')
    elif 'WEBSITE_HOSTNAME' in os.environ:
        # Azure
        print("Loading config.azure")
        app.config.from_object('jboard.config.azure')
    else:
        # Local development
        print("Loading config.local and environment variables from .env file.")
        app.config.from_object('jboard.config.local')

    # register the database commands
    from . import db

    db.init_app(app)

    # apply the blueprints to the app
    from . import auth, job

    app.register_blueprint(auth.bp)
    app.register_blueprint(job.bp)

    app.add_url_rule("/", endpoint="index")

    return app
