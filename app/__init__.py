from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

# создаём объект БД, но пока без привязки к приложению
db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)

# гарантируем, что папка для файлов существует
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# инициализируем БД с приложением
db.init_app(app)

from app.controllers.assets import assets_bp
app.register_blueprint(assets_bp)


@app.route("/")
def index():
    return "AssetHub backend is running. Go to /assets"

