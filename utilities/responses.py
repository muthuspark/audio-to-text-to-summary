from http import HTTPStatus

from flask import jsonify


def json_message(message):
    return {"message": message}


def success(message):
    return jsonify(json_message(message)), HTTPStatus.OK


def error_404(message):
    return jsonify(json_message(message)), HTTPStatus.NOT_FOUND


def error_500(message):
    return jsonify(json_message(message)), HTTPStatus.INTERNAL_SERVER_ERROR
