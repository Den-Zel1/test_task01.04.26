from typing import Optional
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass


class Organization(Base):
    __tablename__ = "organizations"

    # Mapped указывает тип для статического анализа (IDE перестанет подчеркивать)
    # mapped_column задает настройки колонки в БД
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    tin: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    logo_url: Mapped[str | None] = mapped_column()  # Колонка для ссылки
   

