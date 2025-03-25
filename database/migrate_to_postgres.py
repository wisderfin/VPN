import os
import peewee
from models import BaseModel, Server, VPNKey, User, Group

# Подключение к SQLite
sqlite_db = peewee.SqliteDatabase(os.path.join(os.path.dirname(__file__), "database.db"))

# Подключение к PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/vpn_bot')
url = peewee.urlparse(DATABASE_URL)
postgres_db = peewee.PostgresqlDatabase(
    url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port or 5432
)

def migrate_data():
    # Создаем таблицы в PostgreSQL
    postgres_db.create_tables(BaseModel.__subclasses__())

    # Мигрируем данные из SQLite в PostgreSQL
    for model in [Server, VPNKey, User, Group]:
        print(f"Миграция {model.__name__}...")
        for instance in model.select():
            instance.save(force_insert=True)
        print(f"Завершена миграция {model.__name__}")

if __name__ == "__main__":
    migrate_data()
