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

from app.models import Asset, Tag

# ===== Инициализация БД и сидинг =====
def seed_data():
    """Простейший сидер: создаём пару ассетов, если их ещё нет."""
    if Asset.query.first():
        return

    a1 = Asset(
        title="Sci-fi Soldier Concept",
        description="Концепт-арт бойца для sci-fi проекта.",
        asset_type="concept",
        file_path="storage/sci_fi_soldier.png",
        project_name="Project Nova",
        author_name="Artist One",
    )

    a2 = Asset(
        title="Abandoned Hospital Hall 3D",
        description="3D-модель коридора заброшенной больницы.",
        asset_type="3d_model",
        file_path="storage/abandoned_hall.fbx",
        project_name="Abandoned Hospital",
        author_name="Environment Artist",
    )

    db.session.add_all([a1, a2])
    db.session.commit()


with app.app_context():
    db.create_all()
    seed_data()

from app.controllers.assets import assets_bp
from app.controllers.tags import tags_bp

app.register_blueprint(assets_bp)
app.register_blueprint(tags_bp)


@app.route("/")
def index():
    return "AssetHub backend is running. Go to /assets"



