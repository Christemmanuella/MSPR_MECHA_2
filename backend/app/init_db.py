from pathlib import Path
from sqlalchemy import text
from backend.app.database import engine

BASE_DIR = Path(__file__).resolve().parents[2]
SQL_PATH = BASE_DIR / "database" / "init_db.sql"


def init_database():
    with open(SQL_PATH, "r", encoding="utf-8") as file:
        sql_script = file.read()

    with engine.begin() as connection:
        connection.execute(text(sql_script))

    print("Tables SQL créées avec succès")


if __name__ == "__main__":
    init_database()