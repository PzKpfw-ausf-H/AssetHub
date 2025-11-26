from flask import Blueprint, render_template
from app.models import Asset  # импортируем модель

assets_bp = Blueprint("assets", __name__, url_prefix="/assets")


@assets_bp.route("/")
def assets_list():
    # достаём все ассеты из БД
    assets = Asset.query.order_by(Asset.created_at.desc()).all()
    return render_template("assets/list.html", assets=assets)
