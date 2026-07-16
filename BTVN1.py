from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete="CASCADE"), nullable=False)


class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    # Cấu hình Nhiều-Nhiều trực tiếp qua bảng trung gian 'enrollments'
    courses = relationship(
        "Course", 
        secondary="enrollments", 
        back_populates="students"
    )


class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    # Cấu hình Nhiều-Nhiều trực tiếp ngược lại với Student
    students = relationship(
        "Student", 
        secondary="enrollments", 
        back_populates="courses"
    )