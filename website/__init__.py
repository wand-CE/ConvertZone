import os
from flask import Flask
from sqlalchemy import create_engine, inspect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'convert_zone.db'


def create_app():
    from .views import views
    app = Flask(__name__)

    app.register_blueprint(views, url_prefix='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.secret_key = 'your secret'

    db.init_app(app)

    return app


def create_tables(app):
    with app.app_context():
        db.create_all()
        # from website.models.servicos_model import insert_function_names
        # insert_function_names()
        # remove above comment if there's more functions to add to the site
