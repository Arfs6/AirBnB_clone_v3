#!/usr/bin/python3
"""Flask app for AirBnB api"""

from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


# Create a Flask application instance
app = Flask(__name__)

# Register the blueprint app_views
app.register_blueprint(app_views)

# Initialize CORS with the app instance
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


# Declare a method to handle teardown
@app.teardown_appcontext
def teardown(*args):
    """closes the current SQLAchemy session"""
    storage.close()


@app.errorhandler(404)
def pageNotFound(*args):
    """Handler for 404 Not found errors"""
    return ({'error': 'Not found'}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
