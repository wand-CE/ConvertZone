import os
import time
from datetime import timedelta
import schedule
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
DB_NAME = 'convert_zone.db'


def create_app():
    from .auth import auth
    from .views import views
    from .controllers.functions_controller import http_requests

    app = Flask(__name__)

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(http_requests, url_prefix='/api')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.secret_key = 'your secret'
    app.permanent_session_lifetime = timedelta(minutes=30)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['MEDIA'] = os.path.join(BASE_DIR, 'media')

    db.init_app(app)

    start_cleanup_thread(app)

    CSRFProtect(app)

    return app


def create_tables(app):
    with app.app_context():
        db.create_all()
        from website.models.servicos_model import insert_function_names
        insert_function_names()


def delete_old_folders(path_to_check, age_limit_seconds):
    """
    Delete folders that are older than age_limit_seconds.
    """
    import shutil

    current_time = time.time()

    for foldername in os.listdir(path_to_check):
        folder_path = os.path.join(path_to_check, foldername)

        if os.path.isdir(folder_path):
            creation_time = os.path.getctime(folder_path)

            if current_time - creation_time > age_limit_seconds:
                # Remove the folder if it's old enough
                try:
                    shutil.rmtree(folder_path)
                except Exception as e:
                    print(f"Error to delete {folder_path}: {e}")


def run_scheduled_cleanup(app):
    age_limit_seconds = 1860
    path = os.path.join(app.config['MEDIA'], 'temp_users')
    delete_old_folders(path, age_limit_seconds)
    schedule.every(1).minutes.do(delete_old_folders,
                                 path, age_limit_seconds)

    while True:
        schedule.run_pending()
        time.sleep(1)


def start_cleanup_thread(app):
    import threading

    thread = threading.Thread(target=run_scheduled_cleanup, args=(app,))
    thread.daemon = True
    thread.start()
