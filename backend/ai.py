import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def get_settlement_advice(income, emi, outstanding, overdue):
    prompt = f"""
    Monthly Income: {income}
    EMI: {emi}
    Outstanding Amount: {outstanding}
    Overdue Months: {overdue}

    Suggest a loan settlement recommendation in simple English.
    """

    response = model.generate_content(prompt)
    return response.text

