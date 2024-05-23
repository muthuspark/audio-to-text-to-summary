from dotenv import dotenv_values
from flask import Flask
from flask_cors import CORS

from blueprints.auth import auth_routes_blueprint
from blueprints.file_operations import fileio_routes_blueprint
from blueprints.static_routes import static_routes_blueprint
from blueprints.summarization import summarize_routes_blueprint
from logging_config import logger
from utilities.cache import client_cache

config = dotenv_values(".env")

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})
app.config['SECRET_KEY'] = config.get("FLASK_SECRET")
client_cache.init_app(app)

# Register the blueprint
app.register_blueprint(auth_routes_blueprint)
app.register_blueprint(fileio_routes_blueprint)
app.register_blueprint(summarize_routes_blueprint)
app.register_blueprint(static_routes_blueprint)


@app.errorhandler(Exception)  # Catches all exceptions
def handle_all_errors(error):
    error_message = getattr(error, 'message', str(error))  # Handle potential lack of 'message' attribute
    logger.error(error_message)
    return f"An error occurred! Details: {error_message}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.get("SERVICE_PORT"))
