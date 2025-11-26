from flask import Blueprint, render_template

assets_bp = Blueprint("assets", __name__, url_prefix="/assets")


@assets_bp.route("/")
def assets_list():
    # Пока отдаём фейковые данные, позже заменим на данные из БД
    fake_assets = [
        {"id": 1, "title": "Sci-fi Soldier Concept", "type": "concept"},
        {"id": 2, "title": "Abandoned Hospital Hall 3D", "type": "3d_model"},
    ]
    return render_template("assets/list.html", assets=fake_assets)
