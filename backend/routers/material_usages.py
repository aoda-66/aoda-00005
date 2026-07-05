from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import models
from backend.schemas import schemas
from backend.utils.database import get_db
from typing import List

router = APIRouter(prefix="/material_usages", tags=["material_usages"])

@router.get("/", response_model=List[schemas.MaterialUsage])
def read_material_usages(skip: int = 0, limit: int = 100, procedure_id: int = None, material_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.MaterialUsage)
    if procedure_id:
        query = query.filter(models.MaterialUsage.procedure_id == procedure_id)
    if material_id:
        query = query.filter(models.MaterialUsage.material_id == material_id)
    usages = query.offset(skip).limit(limit).all()
    return usages

@router.get("/{usage_id}", response_model=schemas.MaterialUsage)
def read_material_usage(usage_id: int, db: Session = Depends(get_db)):
    db_usage = db.query(models.MaterialUsage).filter(models.MaterialUsage.id == usage_id).first()
    if db_usage is None:
        raise HTTPException(status_code=404, detail="物料使用记录未找到")
    return db_usage

@router.post("/", response_model=schemas.MaterialUsage)
def create_material_usage(usage: schemas.MaterialUsageCreate, db: Session = Depends(get_db)):
    db_procedure = db.query(models.Procedure).filter(models.Procedure.id == usage.procedure_id).first()
    if not db_procedure:
        raise HTTPException(status_code=404, detail="关联工序未找到")
    db_material = db.query(models.Material).filter(models.Material.id == usage.material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="关联物料未找到")
    if db_material.stock_quantity < usage.quantity:
        raise HTTPException(status_code=400, detail="库存不足")
    new_usage = models.MaterialUsage(**usage.dict())
    db_material.stock_quantity -= usage.quantity
    db.add(new_usage)
    db.commit()
    db.refresh(new_usage)
    return new_usage

@router.put("/{usage_id}", response_model=schemas.MaterialUsage)
def update_material_usage(usage_id: int, usage: schemas.MaterialUsageUpdate, db: Session = Depends(get_db)):
    db_usage = db.query(models.MaterialUsage).filter(models.MaterialUsage.id == usage_id).first()
    if db_usage is None:
        raise HTTPException(status_code=404, detail="物料使用记录未找到")
    if "quantity" in usage.dict(exclude_unset=True):
        db_material = db.query(models.Material).filter(models.Material.id == db_usage.material_id).first()
        if db_material:
            db_material.stock_quantity += db_usage.quantity
            if db_material.stock_quantity < usage.quantity:
                raise HTTPException(status_code=400, detail="库存不足")
            db_material.stock_quantity -= usage.quantity
    for key, value in usage.dict(exclude_unset=True).items():
        setattr(db_usage, key, value)
    db.commit()
    db.refresh(db_usage)
    return db_usage

@router.delete("/{usage_id}")
def delete_material_usage(usage_id: int, db: Session = Depends(get_db)):
    db_usage = db.query(models.MaterialUsage).filter(models.MaterialUsage.id == usage_id).first()
    if db_usage is None:
        raise HTTPException(status_code=404, detail="物料使用记录未找到")
    db_material = db.query(models.Material).filter(models.Material.id == db_usage.material_id).first()
    if db_material:
        db_material.stock_quantity += db_usage.quantity
    db.delete(db_usage)
    db.commit()
    return {"message": "物料使用记录已删除"}