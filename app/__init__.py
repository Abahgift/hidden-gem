from flask import Flask

""" Application Factory Function """
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    return app

app = create_app()

from app.routes import auth, traveler, guide, admin, api