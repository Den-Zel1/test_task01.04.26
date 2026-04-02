from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, create_tables
from app.models import Organization

app = FastAPI()

create_tables()


# 1. Создаем функцию-зависимость (аналог контекстного менеджера)
def get_db():
    db = SessionLocal()
    try:
        yield db  # FastAPI передаст эту сессию в эндпоинт
    finally:
        db.close()  # Сессия закроется сама после завершения запроса


# 2. Используем сессию в эндпоинте через Depends
@app.get("/organizations/{org_id}")
def read_organization(org_id: int, db: Session = Depends(get_db)):
    # Работаем с базой через переменную db
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@app.post("/organizations/")
def create_organization(name: str, tin: str, db: Session = Depends(get_db)):
    new_org = Organization(name=name, tin=tin)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org
