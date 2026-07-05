from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str
    user: 'UserResponse'

class TokenData(BaseModel):
    username: Optional[str] = None

class PermissionBase(BaseModel):
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=100)
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int
    created_at: datetime

    model_config = {'from_attributes': True}

class RoleBase(BaseModel):
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=100)
    description: Optional[str] = None
    is_admin: Optional[bool] = False

class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []

class RoleUpdate(RoleBase):
    name: Optional[str] = None
    code: Optional[str] = None
    permission_ids: Optional[List[int]] = []

class Role(RoleBase):
    id: int
    created_at: datetime
    permissions: List[Permission] = []

    model_config = {'from_attributes': True}

class UserBase(BaseModel):
    username: str = Field(..., max_length=100)
    real_name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=50)
    role_id: int
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: Role
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}

class LoginRequest(BaseModel):
    username: str
    password: str

class BookBase(BaseModel):
    book_name: str = Field(..., max_length=200)
    book_code: str = Field(..., max_length=50)
    author: Optional[str] = Field(None, max_length=100)
    dynasty: Optional[str] = Field(None, max_length=50)
    volume_count: Optional[int] = None
    page_count: Optional[int] = None
    storage_location: Optional[str] = Field(None, max_length=200)
    current_status: Optional[str] = Field("待修复", max_length=50)
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    book_name: Optional[str] = None
    book_code: Optional[str] = None

class Book(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}

class DamageBase(BaseModel):
    damage_type: str = Field(..., max_length=50)
    damage_level: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    damage_date: Optional[str] = None

    @validator('damage_date')
    def parse_date(cls, v):
        if v is None:
            return None
        if isinstance(v, date):
            return v
        try:
            return datetime.strptime(v, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('日期格式必须为 YYYY-MM-DD')

class DamageCreate(DamageBase):
    book_id: int

class DamageUpdate(DamageBase):
    damage_type: Optional[str] = None

class Damage(DamageBase):
    id: int
    book_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}

class ProcedureBase(BaseModel):
    procedure_name: str = Field(..., max_length=100)
    procedure_type: Optional[str] = Field(None, max_length=50)
    executor: Optional[str] = Field(None, max_length=100)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration: Optional[int] = None
    notes: Optional[str] = None
    status: Optional[str] = Field("进行中", max_length=20)

    @validator('start_date', 'end_date')
    def parse_date(cls, v):
        if v is None:
            return None
        if isinstance(v, date):
            return v
        try:
            return datetime.strptime(v, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('日期格式必须为 YYYY-MM-DD')

class ProcedureCreate(ProcedureBase):
    book_id: int

class ProcedureUpdate(ProcedureBase):
    procedure_name: Optional[str] = None

class Procedure(ProcedureBase):
    id: int
    book_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}

class MaterialBase(BaseModel):
    material_name: str = Field(..., max_length=100)
    material_code: str = Field(..., max_length=50)
    unit: Optional[str] = Field(None, max_length=20)
    stock_quantity: Optional[float] = Field(0)
    min_stock: Optional[float] = Field(0)
    price: Optional[float] = None
    supplier: Optional[str] = Field(None, max_length=100)
    storage_location: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(MaterialBase):
    material_name: Optional[str] = None
    material_code: Optional[str] = None

class Material(MaterialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}

class MaterialUsageBase(BaseModel):
    quantity: float = Field(..., gt=0)
    usage_date: Optional[str] = None
    notes: Optional[str] = None

    @validator('usage_date')
    def parse_date(cls, v):
        if v is None:
            return None
        if isinstance(v, date):
            return v
        try:
            return datetime.strptime(v, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('日期格式必须为 YYYY-MM-DD')

class MaterialUsageCreate(MaterialUsageBase):
    procedure_id: int
    material_id: int

class MaterialUsageUpdate(MaterialUsageBase):
    pass

class MaterialUsage(MaterialUsageBase):
    id: int
    procedure_id: int
    material_id: int
    created_at: datetime

    model_config = {'from_attributes': True}

class ArchiveBase(BaseModel):
    archive_type: str = Field(..., max_length=50)
    archive_name: str = Field(..., max_length=200)
    file_path: Optional[str] = Field(None, max_length=500)
    file_url: Optional[str] = Field(None, max_length=500)
    upload_date: Optional[str] = None
    description: Optional[str] = None

    @validator('upload_date')
    def parse_date(cls, v):
        if v is None:
            return None
        if isinstance(v, date):
            return v
        try:
            return datetime.strptime(v, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('日期格式必须为 YYYY-MM-DD')

class ArchiveCreate(ArchiveBase):
    book_id: int

class ArchiveUpdate(ArchiveBase):
    archive_type: Optional[str] = None
    archive_name: Optional[str] = None

class Archive(ArchiveBase):
    id: int
    book_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}