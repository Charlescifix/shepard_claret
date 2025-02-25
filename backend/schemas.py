from pydantic import BaseModel, EmailStr
from datetime import date

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
