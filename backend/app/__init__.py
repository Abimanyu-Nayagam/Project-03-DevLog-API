from flask import Flask
from flask_cors import CORS
from .models.db_models import db
from .routes.crud_route import bp as crud_routes_bp
from .routes.export_route import e_bp as export_routes_bp
from .routes.autogen_route import autogen_bp
from .routes.auth_route import auth_bp, jwt
from config.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app) # Enable CORS for all routes to resolve cross-origin issues (React and Flask running on different ports)
    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(crud_routes_bp) #Register the route blueprint
    app.register_blueprint(export_routes_bp) #Register the file export route blueprint
    app.register_blueprint(auth_bp) # Register the auth blueprint
    app.register_blueprint(autogen_bp) # Register the autogen blueprint
    return app