"""Flask Application Factory"""
from flask import Flask
from config import config
import pymysql

def get_db_connection(app):
    return pymysql.connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DB_NAME'],
        cursorclass=pymysql.cursors.DictCursor
    )

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from .routes.auth     import auth_bp
    from .routes.seeker   import seeker_bp
    from .routes.employer import employer_bp
    from .routes.admin    import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(seeker_bp,   url_prefix='/seeker')
    app.register_blueprint(employer_bp, url_prefix='/employer')
    app.register_blueprint(admin_bp,    url_prefix='/admin')

    return app
