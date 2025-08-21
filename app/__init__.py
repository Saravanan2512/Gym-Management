from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Secret key (⚠️ load from env in production)
    app.config["SECRET_KEY"] = "your_secret_key"

    # Database (SQLite for now)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gym.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Alembic sees them
    from app.models import client, package, trainer

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    # from app.routes.payments import payments_bp   # ✅ payments first
    from app.routes.clients import clients_bp     # ✅ clients after payments
    from app.routes.packages import packages_bp
    from app.routes.trainers import trainers_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp)
    # app.register_blueprint(payments_bp, url_prefix="/payments")
    app.register_blueprint(clients_bp, url_prefix="/clients")
    app.register_blueprint(packages_bp, url_prefix="/packages")
    app.register_blueprint(trainers_bp, url_prefix="/trainers")

    return app
