from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.schemas import schemas
from backend.models import models
from backend.utils.database import get_db
from backend.utils.auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from backend.utils.captcha import generate_captcha, verify_captcha

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/captcha")
def get_captcha():
    captcha_id, image_data = generate_captcha()
    return {"captcha_id": captcha_id, "image": image_data.hex()}

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    if not verify_captcha(login_data.captcha_id, login_data.captcha_code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="验证码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    user_response = schemas.UserResponse.from_orm(user)
    return {"access_token": access_token, "token_type": "bearer", "user": user_response}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@router.post("/init")
def init_system(db: Session = Depends(get_db)):
    admin_role = db.query(models.Role).filter(models.Role.code == "admin").first()
    if admin_role:
        raise HTTPException(status_code=400, detail="系统已初始化")
    
    admin_role = models.Role(
        name="超级管理员",
        code="admin",
        description="拥有所有权限的超级管理员角色",
        is_admin=True
    )
    db.add(admin_role)
    db.commit()
    db.refresh(admin_role)
    
    permissions = [
        {"name": "用户管理", "code": "user_manage"},
        {"name": "角色管理", "code": "role_manage"},
        {"name": "权限管理", "code": "permission_manage"},
        {"name": "藏品管理", "code": "book_manage"},
        {"name": "病害存档", "code": "damage_manage"},
        {"name": "工序登记", "code": "procedure_manage"},
        {"name": "物料台账", "code": "material_manage"},
        {"name": "归档查询", "code": "archive_manage"},
    ]
    
    for p in permissions:
        permission = models.Permission(**p)
        db.add(permission)
    db.commit()
    
    admin_user = models.User(
        username="admin",
        password_hash=get_password_hash("123456"),
        real_name="超级管理员",
        role_id=admin_role.id
    )
    db.add(admin_user)
    db.commit()
    
    return {"message": "系统初始化完成，默认管理员账号：admin/123456"}