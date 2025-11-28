# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db.init_app(app)

from app.controllers.assets import assets_bp
app.register_blueprint(assets_bp)

from app.controllers.tags import tags_bp
app.register_blueprint(tags_bp)

@app.route("/")
def index():
    return "AssetHub backend is running. Go to /assets"


