import os

from flask import Flask
from flask_migrate import Migrate

from src.models import db

migrate = Migrate()

# Integrar: SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Marshmallow, JWT e APISpec
def create_app(environment=os.environ['ENVIRONMENT']):
    # create andd configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['DATABASE'] = "instance/database.db"
    app.config.from_object(f'src.app.config.{environment.title()}Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    
    @app.route('/')
    def hello(): 
        return 'hello world!'
    return app