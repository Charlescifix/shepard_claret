from sqlalchemy import Column, Integer, String, Date
from datetime import date
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    role = Column(String(20), nullable=False)  # Consider adding a CHECK constraint at DB level
    date_joined = Column(Date, default=date.today)
