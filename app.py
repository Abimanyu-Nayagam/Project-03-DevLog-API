from flask import Flask
from app.models.db_models import db
from app.routes.route import bp as routes_bp
from config.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Register blueprints
app.register_blueprint(routes_bp) #Register the route blueprint

if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()  # creates tables if they don't exist
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")    
    app.run(debug=True)
