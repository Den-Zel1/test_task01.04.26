import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # Импортируем ВАШ Base из файла моделей

# 1. Загружаем переменные из .env
load_dotenv()

USER = os.getenv("DB_USER", "postgres")
PASSWORD = os.getenv("DB_PASSWORD", "postgres")
NAME = os.getenv("DB_NAME", "postgres")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "5432")

# 2. Формируем актуальный URL
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Зависимость для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Исправленная функция создания таблиц
def create_tables():
    # Импорт модели внутри функции гарантирует, что Base узнает о таблице Organization
    from app.models import Organization
    Base.metadata.create_all(bind=engine)
