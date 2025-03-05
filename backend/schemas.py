from pydantic import BaseModel, EmailStr
from datetime import date

# User schemas remain the same
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int
    date_joined: date

    class Config:
        from_attributes = True

# StudentProfile schemas
class StudentProfileBase(BaseModel):
    grade_level: str
    enrollment_date: date
    guardian_name: str
    guardian_contact: str
    medical_notes: str

class StudentProfileCreate(StudentProfileBase):
    student_id: int

class StudentProfile(StudentProfileBase):
    student_id: int

    class Config:
        from_attributes = True

# TeacherProfile schemas
class TeacherProfileBase(BaseModel):
    subject_specialization: str
    qualification: str
    employment_type: str

class TeacherProfileCreate(TeacherProfileBase):
    teacher_id: int

class TeacherProfile(TeacherProfileBase):
    teacher_id: int

    class Config:
        from_attributes = True

# Department schemas
class DepartmentBase(BaseModel):
    name: str
    head_teacher_id: int

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    department_id: int

    class Config:
        from_attributes = True

# Course schemas
class CourseBase(BaseModel):
    course_name: str
    department_id: int
    description: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    course_id: int

    class Config:
        from_attributes = True
