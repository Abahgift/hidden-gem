from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()

""" Application Factory Function """
def create_app():
    from app.models import db
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py')
    db.init_app(app)
    Migrate(app,db)   # This sets up version control for the Database
    csrf.init_app(app)

    return app

app = create_app()

from app.routes import auth, traveler, guide, admin, api