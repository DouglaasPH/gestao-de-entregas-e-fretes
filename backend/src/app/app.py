import os

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

from src.models import db
from src.db.db import init_app as db_init_app

migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
bcrypt = Bcrypt()

# Integrar: SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Marshmallow, JWT e APISpec
def create_app(environment=os.environ['ENVIRONMENT']):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['DATABASE'] = "instance/database.sqlite"
    app.config.from_object(f'src.app.config.{environment.title()}Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Registra funções de db: close_db e comando init-db
    db_init_app(app)
    
    # register blueprints
    from src.controllers import user, auth, points_of_sale
    
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(points_of_sale.app)
    
    @app.route('/')
    def hello(): 
        return 'hello world!'
    return app