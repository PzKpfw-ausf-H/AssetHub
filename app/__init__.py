from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.controllers.assets import assets_bp  # noqa: E402

app.register_blueprint(assets_bp)


# Можно добавить простой маршрут для /
@app.route("/")
def index():
    # просто редирект или заглушка — пока редирект в /assets сделаем позже,
    # сейчас пусть возвращает текст
    return "AssetHub backend is running. Go to /assets"

