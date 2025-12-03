# tests/conftest.py
import pytest

from app import app, db, seed_data


@pytest.fixture
def app_with_db():
    """
    Тестовый экземпляр приложения.
    """
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_data()

    yield app


@pytest.fixture
def client(app_with_db):
    return app_with_db.test_client()


@pytest.fixture
def app_ctx(app_with_db):
    """
    Контекст приложения
    """
    with app_with_db.app_context():
        yield
