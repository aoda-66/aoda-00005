from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import models
from backend.schemas import schemas
from backend.utils.database import get_db
from typing import List

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="古籍未找到")
    return db_book

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.book_code == book.book_code).first()
    if db_book:
        raise HTTPException(status_code=400, detail="古籍编号已存在")
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="古籍未找到")
    if book.book_code and book.book_code != db_book.book_code:
        existing = db.query(models.Book).filter(models.Book.book_code == book.book_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="古籍编号已存在")
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="古籍未找到")
    db.delete(db_book)
    db.commit()
    return {"message": "古籍已删除"}