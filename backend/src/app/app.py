import os

from flask import Flask

def create_app(environment=os.environ['ENVIRONMENT']):
    # create andd configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f'src.app.config.{environment.title()}Config')
    
    
    @app.route('/')
    def hello(): 
        return 'hello world!'
    return app