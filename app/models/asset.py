from datetime import datetime
from app import db


class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    asset_type = db.Column(db.String(50), nullable=False)  # concept, 3d_model, texture и тд
    file_path = db.Column(db.String(512), nullable=False)
    preview_path = db.Column(db.String(512))
    project_name = db.Column(db.String(255))
    author_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    tags = db.relationship(
        "Tag",
        secondary="asset_tags",
        back_populates="assets"
    )

    def __repr__(self):
        return f"<Asset id={self.id} title={self.title!r}>"
