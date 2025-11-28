# app/controllers/assets.py
from flask import Blueprint, render_template, abort, current_app, request, redirect, url_for, flash
from app.models import Asset, Tag, AssetTag
import os
import uuid
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload

assets_bp = Blueprint("assets", __name__, url_prefix="/assets")


@assets_bp.route("/")
@assets_bp.route("/")
def assets_list():
    tag_filter = request.args.get("tag")

    if tag_filter:
        assets = (
            Asset.query
            .join(Asset.tags)
            .filter(Tag.name == tag_filter)
            .order_by(Asset.created_at.desc())
            .all()
        )
    else:
        assets = Asset.query.order_by(Asset.created_at.desc()).all()

    return render_template("assets/list.html", assets=assets, tag_filter=tag_filter)

@assets_bp.route("/<int:asset_id>")
def asset_detail(asset_id):
    asset = Asset.query.get(asset_id)
    if asset is None:
        abort(404)
    return render_template("assets/detail.html", asset=asset)

# проверка на разрешенный тип файла
def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]

# обработка POST и GET запросов
@assets_bp.route("/upload", methods=["GET"])
def upload_form():
    return render_template("assets/upload.html")


@assets_bp.route("/upload", methods=["POST"])
def upload_asset():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    asset_type = request.form.get("asset_type", "").strip()
    project_name = request.form.get("project_name", "").strip()
    author_name = request.form.get("author_name", "").strip()
    tags_raw = request.form.get("tags", "").strip()

    file = request.files.get("file")

    errors = []

    if not title:
        errors.append("Укажите название ассета.")
    if not asset_type:
        errors.append("Укажите тип ассета.")
    if not file or file.filename == "":
        errors.append("Выберите файл ассета.")
    elif not allowed_file(file.filename):
        errors.append("Недопустимый тип файла.")

    if errors:

        return render_template(
            "assets/upload.html",
            errors=errors,
            form={
                "title": title,
                "description": description,
                "asset_type": asset_type,
                "project_name": project_name,
                "author_name": author_name,
            },
        )

    # Сохраняем файл
    original_name = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{original_name}"
    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, unique_name)
    file.save(file_path)

    # Путь, который будем хранить в БД
    db_path = f"{folder}/{unique_name}"

    from app import db

    asset = Asset(
        title=title,
        description=description,
        asset_type=asset_type,
        file_path=db_path,
        project_name=project_name or None,
        author_name=author_name or None,
    )

    db.session.add(asset)

    # обрабатываем теги
    tags_list = []
    if tags_raw:
        # разбиваем по запятой, убираем пробелы
        tags_list = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]

    # для каждого тега берём существующий или создаём новый
    asset_tags = []
    for tag_name in tags_list:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
            db.session.flush()
        asset_tags.append(tag)

    asset.tags = asset_tags


    db.session.commit()

    # после добавления редиректит на страницу ассета
    return redirect(url_for("assets.asset_detail", asset_id=asset.id))



