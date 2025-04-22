
# Personal Finance Chatbot for Students
# Budgeting, Retirement, and Estate Planning Tool (Web Version)

import json
import streamlit as st

# Assumptions
assumptions = {
    "TCJA_permanent": True,
    "residence_state": "Michigan",
    "social_security_age": 68,
    "social_security_cut_year": 2033,
    "social_security_reduction": 0.30,
    "inflation_rate": 0.03,
    "investment_return_rate": 0.08,
    "ira_vs_roth_ira": ["IRA", "Roth IRA"],
    "education_savings_plan": "529 Plan",
    "estate_valuation_age": 80,
    "cost_of_living_area": "South Bend, IN"
}

st.title("💰 Personal Finance Chatbot for Students")
st.write("Use this tool to build a basic monthly budget and explore planning for retirement and estate goals.")

# Input Section
with st.form("budget_form"):
    st.header("User Profile")
    individual_age = st.number_input("Your Age", min_value=18, max_value=100, value=30)
    spouse_age = st.number_input("Spouse's Age (0 if none)", min_value=0, max_value=100, value=0)
    dep_count = st.number_input("Number of Dependents", min_value=0, max_value=10, value=0)
    dependents = []
    for i in range(dep_count):
        col1, col2 = st.columns(2)
        with col1:
            dep_age = st.number_input(f"Dependent {i+1} Age", min_value=0, max_value=100, key=f"dep_age_{i}")
        with col2:
            dep_rel = st.text_input(f"Dependent {i+1} Relationship", key=f"dep_rel_{i}")
        dependents.append((dep_age, dep_rel))

    st.header("Monthly Income")
    income_individual = st.number_input("Your Monthly Income", min_value=0.0, value=3000.0)
    income_spouse = 0.0
    if spouse_age > 0:
        income_spouse = st.number_input("Spouse's Monthly Income", min_value=0.0, value=2500.0)

    st.header("Monthly Expenses")
    mortgage = st.number_input("Mortgage or Rent", min_value=0.0, value=1000.0)
    groceries = st.number_input("Groceries", min_value=0.0, value=400.0)
    gas = st.number_input("Gas (Transportation)", min_value=0.0, value=150.0)
    electricity = st.number_input("Electricity", min_value=0.0, value=120.0)

    submitted = st.form_submit_button("Submit and Analyze")

if submitted:
    user_profile = {
        "individual_age": individual_age,
        "spouse_age": spouse_age,
        "dependents": dependents,
        "monthly_income": {
            "individual": income_individual,
            "spouse": income_spouse
        },
        "income_changes": []
    }

    monthly_expenses = {
        "housing": {"mortgage_or_rent": mortgage},
        "food": {"groceries": groceries},
        "transportation": {"gas": gas},
        "utilities": {"electricity": electricity}
    }

    total_income = income_individual + income_spouse
    total_expenses = mortgage + groceries + gas + electricity
    disposable_income = total_income - total_expenses

    st.header("📊 Monthly Budget Summary")
    st.write(f"**Total Monthly Income:** ${total_income:,.2f}")
    st.write(f"**Total Monthly Expenses:** ${total_expenses:,.2f}")
    st.write(f"**Disposable Income:** ${disposable_income:,.2f}")

    # Export report
    report = {
        "user_profile": user_profile,
        "monthly_expenses": monthly_expenses
    }
    report_json = json.dumps(report, indent=4)
    st.download_button("Download Budget Report (JSON)", report_json, file_name="budget_report.json")
