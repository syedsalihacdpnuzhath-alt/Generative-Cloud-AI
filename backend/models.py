from sqlalchemy import Column, Integer, String, Float
from database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    monthly_income = Column(Float)
    emi = Column(Float)
    outstanding_amount = Column(Float)
    overdue_months = Column(Integer)