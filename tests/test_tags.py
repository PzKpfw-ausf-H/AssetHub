from app.models import Asset, Tag
from app import db


def test_tags_page_works(client):
    """
    Страница /tags/ отдаётся (даже если тегов пока нет)
    """
    resp = client.get("/tags/")
    assert resp.status_code == 200


def test_asset_tags_are_visible_on_detail(client, app_ctx):
    """
    Если у ассета есть теги, то они отображаются на детальной странице
    """
    # создаём ассет и тег вручную
    asset = Asset(
        title="Tagged asset",
        description="With tag",
        asset_type="concept",
        file_path="storage/test.png",
    )
    tag = Tag(name="test-tag")

    asset.tags.append(tag)
    db.session.add(asset)
    db.session.commit()

    resp = client.get(f"/assets/{asset.id}")
    text = resp.get_data(as_text=True)

    assert resp.status_code == 200
    assert "test-tag" in text
