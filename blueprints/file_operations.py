import os
import uuid
import http
from dotenv import dotenv_values

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename

from blueprints.summarization import summarization_request_queue
from logging_config import logger
from utilities.request_queue import PersistentQueueRequest

config = dotenv_values(".env")

fileio_routes_blueprint = Blueprint('fileio_routes', __name__)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'webm'}


def allowed_file(filename):
    """
    Check if the uploaded file has a valid audio extension.

    Args:
        filename (str): The name of the uploaded file.

    Returns:
        bool: True if the file has a valid audio extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@fileio_routes_blueprint.route('/upload', methods=['POST'])
def upload_audio():
    """
    Flask route for uploading an audio file.

    This route accepts a POST request with an audio file in the 'audio' field of the request files.
    The file must have a valid audio extension (WAV, MP3, WEBM, or FLAC).
    The uploaded file is saved with a unique filename in the 'recordings' directory.

    Returns:
        A JSON response with one of the following cases:
        - 200 OK: If the file is uploaded successfully, with the message and filename in the response.
        - 400 Bad Request: If there is no file part in the request or if the file has an invalid extension.
        - 500 Internal Server Error: If there is an error saving the file.
    """
    if 'audio' not in request.files:
        logger.error('No audio file part in the request')
        return jsonify({'error': 'No audio file part in the request'}), http.HTTPStatus.BAD_REQUEST

    audio_file = request.files['audio']
    recording_name = request.form.get('name')
    if audio_file.filename == '':
        logger.error('No audio file selected for uploading')
        return jsonify({'error': 'No audio file selected for uploading'}), http.HTTPStatus.BAD_REQUEST

    if not allowed_file(audio_file.filename):
        logger.error('Invalid audio file format')
        return jsonify({'error': 'Invalid audio file format'}), http.HTTPStatus.BAD_REQUEST

    unique_filename = create_unique_name(audio_file)
    upload_path = os.path.join(config.get("UPLOAD_FOLDER"), unique_filename)

    try:
        os.makedirs(config.get("UPLOAD_FOLDER"), exist_ok=True)
        audio_file.save(upload_path)
        logger.info(f'Audio file uploaded successfully: {unique_filename}')
        summarization_request_queue.put(PersistentQueueRequest(unique_filename, recording_name))
        return jsonify({'message': 'Audio file uploaded successfully', 'filename': unique_filename}), http.HTTPStatus.OK
    except Exception as e:
        logger.error(f'Error uploading audio file: {e}')
        return jsonify({'error': 'Error uploading audio file'}), http.HTTPStatus.INTERNAL_SERVER_ERROR


def create_unique_name(audio_file):
    """
    Create a unique filename for the uploaded audio file.

    Args:
        audio_file (FileStorage): The uploaded audio file.

    Returns:
        str: A unique filename with the file extension.
    """
    filename = secure_filename(audio_file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
    return unique_filename
