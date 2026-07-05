from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.database import engine, Base
from backend.routers import books, damages, procedures, materials, material_usages, archives, auth, users, roles
from backend.utils.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="古籍修复数字管理平台", description="数字化规范古籍修复全流程", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router, dependencies=[Depends(get_current_active_user)])
app.include_router(roles.router, dependencies=[Depends(get_current_active_user)])
app.include_router(books.router, dependencies=[Depends(get_current_active_user)])
app.include_router(damages.router, dependencies=[Depends(get_current_active_user)])
app.include_router(procedures.router, dependencies=[Depends(get_current_active_user)])
app.include_router(materials.router, dependencies=[Depends(get_current_active_user)])
app.include_router(material_usages.router, dependencies=[Depends(get_current_active_user)])
app.include_router(archives.router, dependencies=[Depends(get_current_active_user)])

@app.get("/")
def root():
    return {"message": "古籍修复数字管理平台 API"}