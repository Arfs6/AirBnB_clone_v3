#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Api for AirBnB Clone"""

from flask import Flask
from os import getenv

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDownAppContext(*args):
    """Refresh storage."""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    if getenv('HBNB_API_PORT') and getenv('HBNB_API_PORT').isdigit():
        port = int(getenv('HBNB_API_PORT'))
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)
