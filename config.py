import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///assethub.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "storage"

    # разрешенные типы
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "obj", "fbx"}
