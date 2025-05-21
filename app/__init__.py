from flask import Flask
from flask_session import Session
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "super_secret_key"
    app.config['SESSION_TYPE'] = 'filesystem'

    Session(app)
    register_routes(app)

    return app
