from flask import Blueprint, render_template
from app.models import Tag

tags_bp = Blueprint("tags", __name__, url_prefix="/tags")

@tags_bp.route("/")
def tags_list():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template("tags/list.html", tags=tags)
