from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.schemas import schemas
from backend.models import models
from backend.utils.database import get_db
from backend.utils.auth import get_current_active_user, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户未找到")
    return db_user

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    role = db.query(models.Role).filter(models.Role.id == user.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="角色不存在")
    
    new_user = models.User(
        username=user.username,
        password_hash=get_password_hash(user.password),
        real_name=user.real_name,
        email=user.email,
        phone=user.phone,
        role_id=user.role_id,
        is_active=user.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户未找到")
    
    if user.username and user.username != db_user.username:
        existing = db.query(models.User).filter(models.User.username == user.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="用户名已存在")
    
    if user.password:
        db_user.password_hash = get_password_hash(user.password)
    
    for key, value in user.dict(exclude_unset=True).items():
        if key != "password":
            setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户未找到")
    
    if db_user.role.is_admin:
        raise HTTPException(status_code=400, detail="超级管理员不可删除")
    
    db.delete(db_user)
    db.commit()
    return {"message": "用户已删除"}