from flask import Flask
from .models.db_models import db
from .routes.route import bp as routes_bp
from .routes.export_route import e_bp as export_routes_bp
from config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(routes_bp) #Register the route blueprint
    app.register_blueprint(export_routes_bp) #Register the file export route blueprint
    return app



