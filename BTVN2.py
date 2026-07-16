from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List

# ==========================================
# PHẦN 1: CẤU HÌNH DATABASE (Thay thế database.py)
# ==========================================
# Nhớ thay thông tin user, password và tên database của bạn vào đây nhé
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/workshop_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# PHẦN 2: ĐỊNH NGHĨA MODELS (Thay thế models.py)
# ==========================================
class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    # Liên kết N-N qua bảng secondary
    workshops = relationship("Workshop", secondary="registrations", back_populates="students")

class Workshop(Base):
    __tablename__ = 'workshops'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    maximum_participants = Column(Integer, nullable=False)
    
    # Đồng bộ ngược lại qua bảng secondary
    students = relationship("Student", secondary="registrations", back_populates="workshops")

class Registration(Base):
    __tablename__ = 'registrations'
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    workshop_id = Column(Integer, ForeignKey('workshops.id'))
    registered_at = Column(DateTime, default=datetime.utcnow)

# ==========================================
# PHẦN 3: ĐỊNH NGHĨA SCHEMAS (Thay thế schemas.py)
# ==========================================
class RegistrationInput(BaseModel):
    student_id: int
    workshop_id: int

class WorkshopBase(BaseModel):
    id: int
    title: str
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    id: int
    full_name: str
    class Config:
        from_attributes = True

class StudentWorkshopsOutput(BaseModel):
    student_id: int = Field(alias='id')
    full_name: str
    workshops: List[WorkshopBase] = []

    class Config:
        from_attributes = True
        populate_by_name = True

class WorkshopStudentsOutput(BaseModel):
    workshop_id: int = Field(alias='id')
    title: str
    students: List[StudentBase] = []

    class Config:
        from_attributes = True
        populate_by_name = True