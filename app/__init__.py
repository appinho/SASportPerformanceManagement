from flask import Flask
from app.main import bp
# from flask_migrate import Migrate

# migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # app.config.from_object('config.Config')
    
    # db.init_app(app)
    # migrate.init_app(app, db)
    
    
    app.register_blueprint(bp)
    
    return app
