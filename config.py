import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key")

    # Если в окружении есть DATABASE_URL — берём её (для Docker / продакшена),
    # иначе используем локальную SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///assethub.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Папка для хранения файлов ассетов
    UPLOAD_FOLDER = "storage"
