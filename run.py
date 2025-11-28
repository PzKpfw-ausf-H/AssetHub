from app import app, db
from app.models import Asset, Tag

def seed_data():
    if Asset.query.first():
        # уже есть хоть один ассет — считаем, что сидить не нужно
        return

    a1 = Asset(
        title="Sci-fi Soldier Concept",
        description="Концепт-арт бойца для sci-fi проекта.",
        asset_type="concept",
        file_path="storage/sci_fi_soldier.png",
        project_name="Project Nova",
        author_name="Artist One",
    )

    a2 = Asset(
        title="Abandoned Hospital Hall 3D",
        description="3D-модель коридора заброшенной больницы.",
        asset_type="3d_model",
        file_path="storage/abandoned_hall.fbx",
        project_name="Abandoned Hospital",
        author_name="Environment Artist",
    )

    db.session.add_all([a1, a2])
    db.session.commit()
    print("Seed: добавлены тестовые ассеты")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()

    app.run(host="0.0.0.0", port=8000, debug=True)



