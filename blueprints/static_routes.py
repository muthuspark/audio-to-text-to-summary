from flask import Blueprint, send_from_directory

"""
Blueprint for static files
"""
static_routes_blueprint = Blueprint('static_routes', __name__)


@static_routes_blueprint.route('/recordings/<path:path>')
def recordings(path):
    """
    Route for serving the index.html file.
    The route is '/', which is the root URL.
    This function serves the 'index.html' file from the 'webapp/dist' directory.
    """
    return send_from_directory('recordings', path)
