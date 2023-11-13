from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import yaml

db = SQLAlchemy()  # Initializing the databaase

def create_app():
    app = Flask(__name__, static_folder='static')
    
    # configuration info will be stored in a yaml file
    with open('config.yaml') as f:
        myconfig = yaml.safe_load(f)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['STATIC_FOLDER'] = 'url_shortener/static'
    app.config['SQLALCHEMY_DATABASE_URI'] = myconfig['dburi']

    db.init_app(app)  # Binding the database with the app

    with app.app_context():
        # Using bp instead of app
        from .routes import bp
        app.register_blueprint(bp)

        db.create_all()  # Creating the database tables

    return app
