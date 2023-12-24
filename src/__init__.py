from flask import Flask
from flask_migrate import Migrate
from src.db import db
from .resources.user import blueprint_user
from .resources.record import blueprint_record
from .resources.category import category_blueprint
from .resources.currency import blueprint_currency
from src.views import blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(blueprint_user)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(blueprint_record)
    app.register_blueprint(blueprint_currency)
    app.register_blueprint(blueprint)
    return app

