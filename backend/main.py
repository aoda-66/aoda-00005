from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.database import engine, Base
from backend.routers import books, damages, procedures, materials, material_usages, archives

Base.metadata.create_all(bind=engine)

app = FastAPI(title="古籍修复数字管理平台", description="数字化规范古籍修复全流程", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(damages.router)
app.include_router(procedures.router)
app.include_router(materials.router)
app.include_router(material_usages.router)
app.include_router(archives.router)

@app.get("/")
def root():
    return {"message": "古籍修复数字管理平台 API"}