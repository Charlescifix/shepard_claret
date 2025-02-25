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


@router.post("/users/", response_model=schemas.User)
def create_user(
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        role: str = Form(...),
        date_joined: str = Form(...),
        db: Session = Depends(get_db)
):
    # Check if email already exists
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


@router.get("/users/count")
def user_count(db: Session = Depends(get_db)):
    count = db.query(models.User).count()
    return {"count": count}


@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users
