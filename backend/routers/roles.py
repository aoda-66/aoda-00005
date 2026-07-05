from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.schemas import schemas
from backend.models import models
from backend.utils.database import get_db
from backend.utils.auth import get_current_active_user

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/", response_model=List[schemas.Role])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    roles = db.query(models.Role).offset(skip).limit(limit).all()
    return roles

@router.get("/{role_id}", response_model=schemas.Role)
def read_role(role_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="角色未找到")
    return db_role

@router.post("/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_role = db.query(models.Role).filter(models.Role.code == role.code).first()
    if db_role:
        raise HTTPException(status_code=400, detail="角色编码已存在")
    
    new_role = models.Role(
        name=role.name,
        code=role.code,
        description=role.description,
        is_admin=role.is_admin or False
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    if role.permission_ids:
        for perm_id in role.permission_ids:
            perm = db.query(models.Permission).filter(models.Permission.id == perm_id).first()
            if perm:
                rp = models.RolePermission(role_id=new_role.id, permission_id=perm_id)
                db.add(rp)
        db.commit()
    
    db.refresh(new_role)
    return new_role

@router.put("/{role_id}", response_model=schemas.Role)
def update_role(role_id: int, role: schemas.RoleUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="角色未找到")
    
    if db_role.is_admin:
        raise HTTPException(status_code=400, detail="超级管理员角色不可修改")
    
    if role.code and role.code != db_role.code:
        existing = db.query(models.Role).filter(models.Role.code == role.code).first()
        if existing:
            raise HTTPException(status_code=400, detail="角色编码已存在")
    
    for key, value in role.dict(exclude_unset=True).items():
        if key != "permission_ids":
            setattr(db_role, key, value)
    
    if role.permission_ids is not None:
        db.query(models.RolePermission).filter(models.RolePermission.role_id == role_id).delete()
        for perm_id in role.permission_ids:
            perm = db.query(models.Permission).filter(models.Permission.id == perm_id).first()
            if perm:
                rp = models.RolePermission(role_id=role_id, permission_id=perm_id)
                db.add(rp)
    
    db.commit()
    db.refresh(db_role)
    return db_role

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="角色未找到")
    
    if db_role.is_admin:
        raise HTTPException(status_code=400, detail="超级管理员角色不可删除")
    
    user_count = db.query(models.User).filter(models.User.role_id == role_id).count()
    if user_count > 0:
        raise HTTPException(status_code=400, detail="该角色下仍有用户，无法删除")
    
    db.query(models.RolePermission).filter(models.RolePermission.role_id == role_id).delete()
    db.delete(db_role)
    db.commit()
    return {"message": "角色已删除"}

@router.get("/permissions/", response_model=List[schemas.Permission])
def read_permissions(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    permissions = db.query(models.Permission).all()
    return permissions