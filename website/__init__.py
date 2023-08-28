from flask import Flask


def create_app():
    from .views import views
    app = Flask(__name__)
    app.register_blueprint(views, url_prefix='/')
    return app
