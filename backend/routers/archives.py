from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import models
from backend.schemas import schemas
from backend.utils.database import get_db
from typing import List

router = APIRouter(prefix="/archives", tags=["archives"])

@router.get("/", response_model=List[schemas.Archive])
def read_archives(skip: int = 0, limit: int = 100, book_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Archive)
    if book_id:
        query = query.filter(models.Archive.book_id == book_id)
    archives = query.offset(skip).limit(limit).all()
    return archives

@router.get("/{archive_id}", response_model=schemas.Archive)
def read_archive(archive_id: int, db: Session = Depends(get_db)):
    db_archive = db.query(models.Archive).filter(models.Archive.id == archive_id).first()
    if db_archive is None:
        raise HTTPException(status_code=404, detail="归档记录未找到")
    return db_archive

@router.post("/", response_model=schemas.Archive)
def create_archive(archive: schemas.ArchiveCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == archive.book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="关联古籍未找到")
    new_archive = models.Archive(**archive.dict())
    db.add(new_archive)
    db.commit()
    db.refresh(new_archive)
    return new_archive

@router.put("/{archive_id}", response_model=schemas.Archive)
def update_archive(archive_id: int, archive: schemas.ArchiveUpdate, db: Session = Depends(get_db)):
    db_archive = db.query(models.Archive).filter(models.Archive.id == archive_id).first()
    if db_archive is None:
        raise HTTPException(status_code=404, detail="归档记录未找到")
    for key, value in archive.dict(exclude_unset=True).items():
        setattr(db_archive, key, value)
    db.commit()
    db.refresh(db_archive)
    return db_archive

@router.delete("/{archive_id}")
def delete_archive(archive_id: int, db: Session = Depends(get_db)):
    db_archive = db.query(models.Archive).filter(models.Archive.id == archive_id).first()
    if db_archive is None:
        raise HTTPException(status_code=404, detail="归档记录未找到")
    db.delete(db_archive)
    db.commit()
    return {"message": "归档记录已删除"}