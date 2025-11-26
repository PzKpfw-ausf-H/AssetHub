from app import app, db
from app.models import Asset, Tag

if __name__ == "__main__":
    # создаём таблицы в БД
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=8000, debug=True)


