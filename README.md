Job Board
======

The basic job board web app built with Flask and Postgres.

## Local development
Create a virtualenv and activate it::

    $ python3 -m venv .venv
    $ . .venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv .venv
    $ .venv\Scripts\activate.bat

Install dependencies::

    $ pip install -r requirements.txt

Rename .env.sample to .env and modify it with your own values.

Run
---

.. code-block:: text

    $ flask init-db
    $ flask run

Open http://127.0.0.1:5000 in a browser.

## Google App Engine
Read [GCP Guide](GCP.md) for more information.