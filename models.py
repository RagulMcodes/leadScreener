from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, column
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "main"

    phone_number = Column(String, primary_key=True, index=True)
    state = Column(Integer, default=1)
    Name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    Area = Column(String, nullable=True)
    Loan_Type = Column(String, nullable=True)
    Cibil_checked = Column(Boolean, nullable=True)
    is_property_approved = Column(Boolean, nullable=True)
    existing_loans = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)


