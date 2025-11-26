from app import db


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    assets = db.relationship(
        "Asset",
        secondary="asset_tags",
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag id={self.id} name={self.name!r}>"


class AssetTag(db.Model):
    __tablename__ = "asset_tags"

    asset_id = db.Column(
        db.Integer,
        db.ForeignKey("assets.id", ondelete="CASCADE"),
        primary_key=True
    )
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True
    )
