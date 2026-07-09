from database import engine
from ai import get_settlement_advice
from models import Base
from ai import generate_negotiation_letter
from dotenv import load_dotenv
import os
import google.generativeai as genai
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(GEMINI_API_KEY)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
Base.metadata.create_all(bind=engine)

class Loan(BaseModel):
    monthly_income: float
    emi: float
    outstanding_amount: float
overdue_months: int

@app.get("/")
def home():
    return {"message": "Welcome to FinRelief AI Platform"}

@app.get("/health")
def health():
    return {"status": "Running"}

@app.post("/financial-analysis")
def financial_analysis(data: Loan):
    emi_ratio = (data.emi / data.monthly_income) * 100
    monthly_surplus = data.monthly_income - data.emi

    if emi_ratio < 30:
        stress = "Low"
    elif emi_ratio < 50:
        stress = "Medium"
    else:
        stress = "High"

    return {
        "EMI Ratio": round(emi_ratio, 2),
        "Monthly Surplus": monthly_surplus,
        "Debt Stress": stress
    }
@app.post("/settlement")
def settlement(data: Loan):
    if data.overdue_months > 12:
        settlement = "60% Settlement Recommended"
    elif data.overdue_months >= 6:
        settlement = "70% Settlement Recommended"
    else:
        settlement = "85% Settlement Recommended"

    return {
        "Outstanding Amount": data.outstanding_amount,
        "Settlement Recommendation": settlement
    }
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
@app.post("/generate-letter")
def generate_letter(data: Loan):
    loan_details = f"""
    Monthly Income: {data.monthly_income}
    EMI: {data.emi}
    Outstanding Amount: {data.outstanding_amount}
    Overdue Months: {data.overdue_months}
    """

    letter = generate_negotiation_letter(loan_details)

    return {
        "letter": letter
    }
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "Backend is working!"}
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str

@app.post("/register")
def register(user: User):
    return {
        "message": "Registration Successful",
        "user": user
    }
@app.post("/settlement")
def settlement(loan: Loan):
    advice = get_settlement_advice(
        loan.monthly_income,
        loan.emi,
        loan.outstanding_amount,
        loan.overdue_months
    )

    return {
        "advice": advice
    }