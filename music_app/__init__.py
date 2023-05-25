from flask import Flask
from flask_migrate import Migrate

from .config import Config
from .extentions import db
from .routers import main


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(Config)
    
    db.init_app(app)

    migrate = Migrate(app, db)

    app.register_blueprint(main)

    return app