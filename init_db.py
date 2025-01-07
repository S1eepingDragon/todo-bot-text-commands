from database import engine
from models import Base
import os

def init_db():
    """Создание таблиц в базе данных, если они не существуют."""
    if not os.path.exists("./data"):
        os.makedirs("./data")

    print("Инициализация базы данных...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы!")


if __name__ == "__main__":
    init_db()
