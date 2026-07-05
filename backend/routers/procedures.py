from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import models
from backend.schemas import schemas
from backend.utils.database import get_db
from typing import List

router = APIRouter(prefix="/procedures", tags=["procedures"])

@router.get("/", response_model=List[schemas.Procedure])
def read_procedures(skip: int = 0, limit: int = 100, book_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Procedure)
    if book_id:
        query = query.filter(models.Procedure.book_id == book_id)
    procedures = query.offset(skip).limit(limit).all()
    return procedures

@router.get("/{procedure_id}", response_model=schemas.Procedure)
def read_procedure(procedure_id: int, db: Session = Depends(get_db)):
    db_procedure = db.query(models.Procedure).filter(models.Procedure.id == procedure_id).first()
    if db_procedure is None:
        raise HTTPException(status_code=404, detail="工序记录未找到")
    return db_procedure

@router.post("/", response_model=schemas.Procedure)
def create_procedure(procedure: schemas.ProcedureCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == procedure.book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="关联古籍未找到")
    new_procedure = models.Procedure(**procedure.dict())
    db.add(new_procedure)
    db.commit()
    db.refresh(new_procedure)
    return new_procedure

@router.put("/{procedure_id}", response_model=schemas.Procedure)
def update_procedure(procedure_id: int, procedure: schemas.ProcedureUpdate, db: Session = Depends(get_db)):
    db_procedure = db.query(models.Procedure).filter(models.Procedure.id == procedure_id).first()
    if db_procedure is None:
        raise HTTPException(status_code=404, detail="工序记录未找到")
    for key, value in procedure.dict(exclude_unset=True).items():
        setattr(db_procedure, key, value)
    db.commit()
    db.refresh(db_procedure)
    return db_procedure

@router.delete("/{procedure_id}")
def delete_procedure(procedure_id: int, db: Session = Depends(get_db)):
    db_procedure = db.query(models.Procedure).filter(models.Procedure.id == procedure_id).first()
    if db_procedure is None:
        raise HTTPException(status_code=404, detail="工序记录未找到")
    db.delete(db_procedure)
    db.commit()
    return {"message": "工序记录已删除"}