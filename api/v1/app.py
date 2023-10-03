#!/usr/bin/python3
"""flask app initial file"""

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''Handle not found error'''
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    # getenv returns a string and port is an int
    # THREADED is set to true so it can serve multiple requests at once
    app.run(host=host, port=port, threaded=True)
