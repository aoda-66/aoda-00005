from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.utils.database import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    permissions = relationship("RolePermission", back_populates="role")
    users = relationship("User", back_populates="role")

class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False, index=True)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", backref="role_permissions")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(500), nullable=False)
    real_name = Column(String(100))
    email = Column(String(200))
    phone = Column(String(50))
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    role = relationship("Role", back_populates="users")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String(200), nullable=False, index=True)
    book_code = Column(String(50), unique=True, nullable=False, index=True)
    author = Column(String(100))
    dynasty = Column(String(50))
    volume_count = Column(Integer)
    page_count = Column(Integer)
    storage_location = Column(String(200))
    current_status = Column(String(50), default="待修复")
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    damages = relationship("Damage", back_populates="book", cascade="all, delete-orphan")
    procedures = relationship("Procedure", back_populates="book", cascade="all, delete-orphan")
    archives = relationship("Archive", back_populates="book", cascade="all, delete-orphan")

class Damage(Base):
    __tablename__ = "damages"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    damage_type = Column(String(50), nullable=False)
    damage_level = Column(String(20))
    location = Column(String(100))
    description = Column(Text)
    damage_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    book = relationship("Book", back_populates="damages")

class Procedure(Base):
    __tablename__ = "procedures"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    procedure_name = Column(String(100), nullable=False)
    procedure_type = Column(String(50))
    executor = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    duration = Column(Integer)
    notes = Column(Text)
    status = Column(String(20), default="进行中")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    book = relationship("Book", back_populates="procedures")
    material_usages = relationship("MaterialUsage", back_populates="procedure", cascade="all, delete-orphan")

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    material_name = Column(String(100), nullable=False, index=True)
    material_code = Column(String(50), unique=True, nullable=False)
    unit = Column(String(20))
    stock_quantity = Column(Float, default=0)
    min_stock = Column(Float, default=0)
    price = Column(Float)
    supplier = Column(String(100))
    storage_location = Column(String(200))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usages = relationship("MaterialUsage", back_populates="material", cascade="all, delete-orphan")

class MaterialUsage(Base):
    __tablename__ = "material_usages"

    id = Column(Integer, primary_key=True, index=True)
    procedure_id = Column(Integer, ForeignKey("procedures.id"), nullable=False, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    usage_date = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    procedure = relationship("Procedure", back_populates="material_usages")
    material = relationship("Material", back_populates="usages")

class Archive(Base):
    __tablename__ = "archives"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    archive_type = Column(String(50), nullable=False)
    archive_name = Column(String(200), nullable=False)
    file_path = Column(String(500))
    file_url = Column(String(500))
    upload_date = Column(Date)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    book = relationship("Book", back_populates="archives")