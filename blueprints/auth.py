import datetime
from functools import wraps

import jwt
from dotenv import dotenv_values
from flask import Blueprint, jsonify
from flask import redirect, request
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient

config = dotenv_values(".env")

configuration = Configuration(host=config.get("KINDE_DOMAIN"))
kinde_api_client_params = {
    "configuration": configuration,
    "domain": config.get("KINDE_DOMAIN"),
    "client_id": config.get("KINDE_CLIENT_ID"),
    "client_secret": config.get("KINDE_CLIENT_SECRET"),
    "grant_type": GrantType.AUTHORIZATION_CODE,
    "callback_url": config.get("KINDE_CALLBACK")
}

kinde_client = KindeApiClient(**kinde_api_client_params)

kinde_client.logout(redirect_to=config.get("KINDE_POST_LOGOUT_REDIRECT_URL"))

auth_routes_blueprint = Blueprint('auth', __name__)

user_clients = {}


def get_user_id(auth_header):
    token = auth_header.split()[1]  # Extract token from "Bearer <token>" format
    data = jwt.decode(token, config.get("FLASK_SECRET"), algorithms=['HS256'])
    return data['user_id']


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Missing token'}), 401
        try:
            get_user_id(auth_header)
            # client = user_clients[get_user_id(auth_header)]
            # if not client.is_authenticated():
            #     return jsonify({'message': 'Invalid token'}), 403
        except jwt.DecodeError:
            return jsonify({'message': 'Invalid token'}), 403
        return f(*args, **kwargs)

    return decorated


@auth_routes_blueprint.route("/login")
def login():
    return redirect(kinde_client.get_login_url())


@auth_routes_blueprint.route("/register")
def register():
    return redirect(kinde_client.get_register_url())


@auth_routes_blueprint.route("/logout")
def logout():
    return redirect(
        kinde_client.logout(redirect_to="/")
    )


@auth_routes_blueprint.route('/callback', methods=['GET'])
def callback():
    kinde_client.fetch_token(authorization_response=request.url)
    user = kinde_client.get_user_details()
    # print(configuration.access_token)
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=600),  # JWT expiration time
        'iat': datetime.datetime.utcnow(),  # Issued at time
        'user_id': user.get("id")
    }
    user_clients[user.get("id")] = kinde_client
    token = jwt.encode(payload, config.get("FLASK_SECRET"), algorithm='HS256')
    return redirect(f"http://localhost:8080/home?token={token}")
