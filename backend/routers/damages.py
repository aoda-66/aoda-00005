from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import models
from backend.schemas import schemas
from backend.utils.database import get_db
from typing import List

router = APIRouter(prefix="/damages", tags=["damages"])

@router.get("/", response_model=List[schemas.Damage])
def read_damages(skip: int = 0, limit: int = 100, book_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Damage)
    if book_id:
        query = query.filter(models.Damage.book_id == book_id)
    damages = query.offset(skip).limit(limit).all()
    return damages

@router.get("/{damage_id}", response_model=schemas.Damage)
def read_damage(damage_id: int, db: Session = Depends(get_db)):
    db_damage = db.query(models.Damage).filter(models.Damage.id == damage_id).first()
    if db_damage is None:
        raise HTTPException(status_code=404, detail="病害记录未找到")
    return db_damage

@router.post("/", response_model=schemas.Damage)
def create_damage(damage: schemas.DamageCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == damage.book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="关联古籍未找到")
    new_damage = models.Damage(**damage.dict())
    db.add(new_damage)
    db.commit()
    db.refresh(new_damage)
    return new_damage

@router.put("/{damage_id}", response_model=schemas.Damage)
def update_damage(damage_id: int, damage: schemas.DamageUpdate, db: Session = Depends(get_db)):
    db_damage = db.query(models.Damage).filter(models.Damage.id == damage_id).first()
    if db_damage is None:
        raise HTTPException(status_code=404, detail="病害记录未找到")
    for key, value in damage.dict(exclude_unset=True).items():
        setattr(db_damage, key, value)
    db.commit()
    db.refresh(db_damage)
    return db_damage

@router.delete("/{damage_id}")
def delete_damage(damage_id: int, db: Session = Depends(get_db)):
    db_damage = db.query(models.Damage).filter(models.Damage.id == damage_id).first()
    if db_damage is None:
        raise HTTPException(status_code=404, detail="病害记录未找到")
    db.delete(db_damage)
    db.commit()
    return {"message": "病害记录已删除"}