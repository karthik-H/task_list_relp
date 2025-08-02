import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database with fallback to SQLite
database_url = os.environ.get("DATABASE_URL")
if database_url and "ep-raspy-king-a5t518cr.us-east-2.aws.neon.tech" in database_url:
    # The old Neon endpoint is disabled, fall back to SQLite
    logging.warning("Detected disabled Neon endpoint, falling back to SQLite")
    database_url = "sqlite:///tasktracker.db"
elif not database_url:
    database_url = "sqlite:///tasktracker.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# Configure engine options based on database type
if database_url.startswith("postgresql"):
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
else:
    # SQLite doesn't need connection pooling
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models so their tables will be created
    import models
    
    # Create all tables
    db.create_all()
    
    # Import and register routes
    import routes
