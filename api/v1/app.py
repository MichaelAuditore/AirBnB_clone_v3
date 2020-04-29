#!/usr/bin/python3
"""Module to implement Blueprint and flask to create API"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import environ

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """Close an instance of session in SQLAlchemy"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Return json when page not found """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=environ.get("HBNB_API_HOST"),
            port=environ.get("HBNB_API_PORT"),
            threaded=True)
