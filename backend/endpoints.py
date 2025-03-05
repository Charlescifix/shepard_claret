from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from backend import models, schemas, database
import datetime

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Retrieve all users ordered by date_joined
@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.date_joined).offset(skip).limit(limit).all()
    return users


@router.get("/users/count")
def user_count(db: Session = Depends(get_db)):
    count = db.query(models.User).count()
    return {"count": count}


@router.post("/users/", response_model=schemas.User)
def create_user(
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        role: str = Form(...),
        date_joined: str = Form(...),
        db: Session = Depends(get_db)
):
    # Check if the user already exists by email
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        parsed_date = datetime.date.fromisoformat(date_joined)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format for date_joined. Use YYYY-MM-DD.")

    new_user = models.User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        role=role,
        date_joined=parsed_date
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Endpoint to create Student Profile
@router.post("/student-profile/", response_model=schemas.StudentProfile)
def create_student_profile(
        student_id: int = Form(...),
        grade_level: str = Form(...),
        enrollment_date: str = Form(...),
        guardian_name: str = Form(...),
        guardian_contact: str = Form(...),
        medical_notes: str = Form(...),
        db: Session = Depends(get_db)
):
    try:
        parsed_enrollment_date = datetime.date.fromisoformat(enrollment_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format for enrollment_date. Use YYYY-MM-DD.")

    user = db.query(models.User).filter(models.User.user_id == student_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_profile = db.query(models.StudentProfile).filter(models.StudentProfile.student_id == student_id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Student profile already exists")

    profile = models.StudentProfile(
        student_id=student_id,
        grade_level=grade_level,
        enrollment_date=parsed_enrollment_date,
        guardian_name=guardian_name,
        guardian_contact=guardian_contact,
        medical_notes=medical_notes
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


# Endpoint to create Teacher Profile
@router.post("/teacher-profile/", response_model=schemas.TeacherProfile)
def create_teacher_profile(
        teacher_id: int = Form(...),
        subject_specialization: str = Form(...),
        qualification: str = Form(...),
        employment_type: str = Form(...),
        db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.user_id == teacher_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_profile = db.query(models.TeacherProfile).filter(models.TeacherProfile.teacher_id == teacher_id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Teacher profile already exists")

    profile = models.TeacherProfile(
        teacher_id=teacher_id,
        subject_specialization=subject_specialization,
        qualification=qualification,
        employment_type=employment_type
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


# Endpoint to create Department
@router.post("/departments/", response_model=schemas.Department)
def create_department(
        name: str = Form(...),
        head_teacher_id: int = Form(...),
        db: Session = Depends(get_db)
):
    head_teacher = db.query(models.User).filter(models.User.user_id == head_teacher_id).first()
    if not head_teacher:
        raise HTTPException(status_code=404, detail="Head teacher not found")

    department = models.Department(
        name=name,
        head_teacher_id=head_teacher_id
    )
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


# Endpoint to create Course
@router.post("/courses/", response_model=schemas.Course)
def create_course(
        course_name: str = Form(...),
        department_id: int = Form(...),
        description: str = Form(...),
        db: Session = Depends(get_db)
):
    department = db.query(models.Department).filter(models.Department.department_id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    course = models.Course(
        course_name=course_name,
        department_id=department_id,
        description=description
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
