from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import date


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    role = Column(String(20), nullable=False)
    date_joined = Column(Date, default=date.today)

    # One-to-one relationships
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    teacher_profile = relationship("TeacherProfile", back_populates="user", uselist=False)


class StudentProfile(Base):
    __tablename__ = "student_profile"
    student_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    grade_level = Column(String(20))
    enrollment_date = Column(Date)
    guardian_name = Column(String(100))
    guardian_contact = Column(String(20))
    medical_notes = Column(Text)

    # Relationship back to User
    user = relationship("User", back_populates="student_profile")


class TeacherProfile(Base):
    __tablename__ = "teacher_profile"
    teacher_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    subject_specialization = Column(String(100))
    qualification = Column(Text)
    employment_type = Column(String(50))

    # Relationship back to User
    user = relationship("User", back_populates="teacher_profile")


class Department(Base):
    __tablename__ = "departments"
    department_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    head_teacher_id = Column(Integer, ForeignKey("users.user_id"))

    # One-to-many relationship with courses
    courses = relationship("Course", back_populates="department")


class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    description = Column(Text)

    # Relationship back to Department
    department = relationship("Department", back_populates="courses")
