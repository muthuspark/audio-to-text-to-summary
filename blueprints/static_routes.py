from flask import Blueprint, send_from_directory

"""
Blueprint for static routes.
"""
static_routes_blueprint = Blueprint('routes', __name__)


@static_routes_blueprint.route('/css/<path:path>')
def serve_css(path):
    """
    Route for serving CSS files.
    The route is '/css/<path:path>', where <path:path> is a dynamic segment
    that matches any path after '/css/'.
    This function serves the requested CSS file from the 'webapp/dist/css' directory.
    """
    return send_from_directory('webapp/dist/css', path)


@static_routes_blueprint.route('/js/<path:path>')
def serve_js(path):
    """
    Route for serving JavaScript files.
    The route is '/js/<path:path>', where <path:path> is a dynamic segment
    that matches any path after '/js/'.
    This function serves the requested JavaScript file from the 'webapp/dist/js' directory.
    """
    return send_from_directory('webapp/dist/js', path)


@static_routes_blueprint.route('/recordings/<path:path>')
def recordings(path):
    """
    Route for serving the index.html file.
    The route is '/', which is the root URL.
    This function serves the 'index.html' file from the 'webapp/dist' directory.
    """
    return send_from_directory('recordings', path)


@static_routes_blueprint.route('/')
def index():
    """
    Route for serving the index.html file.
    The route is '/', which is the root URL.
    This function serves the 'index.html' file from the 'webapp/dist' directory.
    """
    return send_from_directory('webapp/dist', "index.html")
