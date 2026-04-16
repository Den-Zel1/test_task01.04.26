import uuid
import pathlib
from fastapi import FastAPI, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import SessionLocal, create_tables
from app.models import Organization
from app.storage import storage  # Ваш обновленный класс

app = FastAPI()
create_tables()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/organizations/{org_id}/logo")
async def upload_logo(
    org_id: int,
    file: UploadFile,
    db: Session = Depends(get_db)
):
    # 1. Ищем организацию
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")

    # 2. Генерируем путь
    ext = pathlib.Path(file.filename).suffix
    unique_key = f"logos/{uuid.uuid4()}{ext}"

    try:
        # 3. Грузим в MinIO (передаем file.file — это поток!)
        # Важно: вызываем .file, а не .read()
        file_url = await storage.upload_file(
            file_obj=file.file,
            bucket="my-bucket",
            key=unique_key,
            content_type=file.content_type
        )

        # 4. Сохраняем ссылку в БД
        org.logo_url = file_url
        db.commit()
        db.refresh(org)

        return {"id": org.id, "logo_url": org.logo_url}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()
