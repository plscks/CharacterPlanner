from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import config


db = SQLAlchemy()
sess = Session()


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder='static',
        static_url_path=''
        )
    app.config.from_object(config.Config)

    # initialize database
    db.init_app(app)
    db.reflect(app=app)
    app.db = db
    sess.init_app(app)
    with app.app_context():
        from . import routes, forms, models, services
        return app