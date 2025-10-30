from flask import Flask
from .models.db_models import db
from .routes.route import bp as routes_bp
from config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(routes_bp) #Register the route blueprint
    return app



