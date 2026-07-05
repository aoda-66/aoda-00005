from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import models
from backend.schemas import schemas
from backend.utils.database import get_db
from typing import List

router = APIRouter(prefix="/materials", tags=["materials"])

@router.get("/", response_model=List[schemas.Material])
def read_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    materials = db.query(models.Material).offset(skip).limit(limit).all()
    return materials

@router.get("/{material_id}", response_model=schemas.Material)
def read_material(material_id: int, db: Session = Depends(get_db)):
    db_material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="物料未找到")
    return db_material

@router.post("/", response_model=schemas.Material)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    db_material = db.query(models.Material).filter(models.Material.material_code == material.material_code).first()
    if db_material:
        raise HTTPException(status_code=400, detail="物料编号已存在")
    new_material = models.Material(**material.dict())
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material

@router.put("/{material_id}", response_model=schemas.Material)
def update_material(material_id: int, material: schemas.MaterialUpdate, db: Session = Depends(get_db)):
    db_material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="物料未找到")
    if material.material_code and material.material_code != db_material.material_code:
        existing = db.query(models.Material).filter(models.Material.material_code == material.material_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="物料编号已存在")
    for key, value in material.dict(exclude_unset=True).items():
        setattr(db_material, key, value)
    db.commit()
    db.refresh(db_material)
    return db_material

@router.delete("/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    db_material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="物料未找到")
    db.delete(db_material)
    db.commit()
    return {"message": "物料已删除"}

@router.get("/low_stock/", response_model=List[schemas.Material])
def get_low_stock_materials(db: Session = Depends(get_db)):
    materials = db.query(models.Material).filter(models.Material.stock_quantity <= models.Material.min_stock).all()
    return materials