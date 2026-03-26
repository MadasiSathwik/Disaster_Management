from flask_sqlalchemy import SQLAlchemy

# Initialize global extension instances.
# They are imported in application factory (app.py) and initialized there.

# Database abstraction
# NOTE: we call db.init_app(app) from create_app().
db = SQLAlchemy()

# TODO: Add Flask-Migrate (Alembic) for database migrations
# from flask_migrate import Migrate
# migrate = Migrate()
# TODO: Add LoginManager, Mail, etc.
