import io

from app.models import Asset


def test_assets_list_contains_seed_data(client):
    """
    Страница /assets/ отдаётся и содержит ассеты
    """
    resp = client.get("/assets/")
    assert resp.status_code == 200
    assert b"Sci-fi Soldier Concept" in resp.data
    assert b"Abandoned Hospital Hall 3D" in resp.data


def test_asset_detail_existing(client, app_ctx):
    """
    Детальная страница существующего ассета отдаётся с кодом 200
    """
    # Берём любой ассет из БД
    asset = Asset.query.first()
    resp = client.get(f"/assets/{asset.id}")
    assert resp.status_code == 200
    assert asset.title.encode("utf-8") in resp.data


def test_asset_detail_not_found(client):
    """
    Для несуществующего id возвращается 404
    """
    resp = client.get("/assets/999999")
    assert resp.status_code == 404


def test_upload_without_file_shows_errors(client):
    """
    При попытке загрузки без файла возвращается форма с ошибкой
    """
    data = {
        "title": "Test asset",
        "description": "Desc",
        "asset_type": "3d_model",
        "project_name": "Proj",
        "author_name": "Author",
    }

    resp = client.post(
        "/assets/upload",
        data=data,
        follow_redirects=True,
    )

    assert resp.status_code == 200
    assert "Выберите файл ассета." in resp.get_data(as_text=True)


def test_upload_and_download_flow(client, app_ctx):
    """
    Полный сценарий
    """
    initial_count = Asset.query.count()

    file_data = io.BytesIO(b"dummy binary data")
    data = {
        "title": "Uploaded asset",
        "description": "Via test",
        "asset_type": "3d_model",
        "project_name": "TestProj",
        "author_name": "Tester",
        "tags": "test, upload",
        "file": (file_data, "model.fbx"),
    }

    # Загружаем ассет
    resp = client.post(
        "/assets/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert resp.status_code in (302, 303)
    assert "/assets/" in resp.headers["Location"]

    new_count = Asset.query.count()
    assert new_count == initial_count + 1

    asset = Asset.query.order_by(Asset.id.desc()).first()

    # Проверяем скачивание
    resp_download = client.get(f"/assets/{asset.id}/download")
    assert resp_download.status_code == 200
    assert "attachment" in resp_download.headers.get("Content-Disposition", "")
