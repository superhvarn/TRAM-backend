from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initializing the databaase

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['STATIC_FOLDER'] = 'url_shortener/static'

    db.init_app(app)  # Binding the database with the app

    with app.app_context():
        # Using bp instead of app
        from .routes import bp
        app.register_blueprint(bp)

        db.create_all()  # Creating the database tables

    return app
