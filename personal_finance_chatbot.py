# Personal Finance Chatbot for Students
# Budgeting, Retirement, and Estate Planning Tool (Web Version)

import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
st.write("Use this tool to build a detailed monthly budget and explore planning for retirement and estate goals.")

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
    mortgage = st.number_input("Mortgage or Rent", min_value=0.0, value=3000.0)
    property_tax = st.number_input("Property Taxes", min_value=0.0, value=500.0)
    household_repairs = st.number_input("Household Repairs", min_value=0.0, value=100.0)
    hoa_fees = st.number_input("HOA Fees", min_value=0.0, value=50.0)

    car_payment = st.number_input("Car Payment", min_value=0.0, value=300.0)
    gas = st.number_input("Gas (Transportation)", min_value=0.0, value=150.0)
    car_maintenance = st.number_input("Car Maintenance", min_value=0.0, value=60.0)
    car_insurance = st.number_input("Auto Insurance", min_value=0.0, value=100.0)

    groceries = st.number_input("Groceries", min_value=0.0, value=400.0)
    restaurants = st.number_input("Restaurants", min_value=0.0, value=150.0)
    pet_food = st.number_input("Pet Food", min_value=0.0, value=50.0)

    electricity = st.number_input("Electricity", min_value=0.0, value=120.0)
    water = st.number_input("Water", min_value=0.0, value=40.0)
    garbage = st.number_input("Garbage", min_value=0.0, value=30.0)
    phones = st.number_input("Phone Bills", min_value=0.0, value=80.0)
    internet = st.number_input("Internet", min_value=0.0, value=60.0)

    health_insurance = st.number_input("Health Insurance", min_value=0.0, value=400.0)
    medical_expenses = st.number_input("Other Medical Expenses", min_value=0.0, value=100.0)

    childcare = st.number_input("Childcare/Education", min_value=0.0, value=200.0)
    entertainment = st.number_input("Entertainment", min_value=0.0, value=150.0)
    subscriptions = st.number_input("Subscriptions (e.g., Netflix, Hulu)", min_value=0.0, value=30.0)

    savings = st.number_input("Savings (Monthly)", min_value=0.0, value=300.0)
    retirement_savings = st.number_input("Retirement Contributions", min_value=0.0, value=200.0)

    st.header("Retirement Planning")
    retirement_age = st.number_input("Target Retirement Age", min_value=50, max_value=75, value=68)
    current_retirement_balance = st.number_input("Current Retirement Savings Balance", min_value=0.0, value=50000.0)
    additional_ira_contributions = st.number_input("Additional IRA/Roth IRA Contributions (Monthly)", min_value=0.0, value=100.0)

    st.header("Estate Planning")
    expected_estate_value = st.number_input("Expected Estate Value at Age 80", min_value=0.0, value=500000.0)
    beneficiaries = st.text_area("List of Beneficiaries and Shares (e.g., Child A - 50%, Child B - 50%)")

    submitted = st.form_submit_button("Submit and Analyze")

if submitted:
    current_age = individual_age
    years = list(range(current_age, min(current_age + 45, 101)))
    retirement_balance = current_retirement_balance
    retirement_forecast = []

    for year in years:
        retirement_balance *= (1 + assumptions["investment_return_rate"])
        retirement_balance += (additional_ira_contributions + retirement_savings) * 12
        retirement_forecast.append({"Age": year, "Retirement Balance": retirement_balance})

    df_retirement = pd.DataFrame(retirement_forecast)
    st.header("📈 Retirement Forecast (up to 45 years)")
    st.line_chart(df_retirement.set_index("Age"))

    st.header("📊 Monthly Budget Summary")
    total_income = income_individual + income_spouse
    total_expenses = sum([
        mortgage, property_tax, household_repairs, hoa_fees,
        car_payment, gas, car_maintenance, car_insurance,
        groceries, restaurants, pet_food,
        electricity, water, garbage, phones, internet,
        health_insurance, medical_expenses,
        childcare, entertainment, subscriptions,
        savings, retirement_savings
    ])
    disposable_income = total_income - total_expenses
    st.write(f"**Total Monthly Income:** ${total_income:,.2f}")
    st.write(f"**Total Monthly Expenses:** ${total_expenses:,.2f}")
    st.write(f"**Disposable Income:** ${disposable_income:,.2f}")

    # Export report
    user_profile = {
        "individual_age": individual_age,
        "spouse_age": spouse_age,
        "dependents": dependents,
        "monthly_income": {
            "individual": income_individual,
            "spouse": income_spouse
        },
        "income_changes": [],
        "retirement": {
            "target_age": retirement_age,
            "current_balance": current_retirement_balance,
            "monthly_contributions": additional_ira_contributions
        },
        "estate": {
            "value_at_80": expected_estate_value,
            "beneficiaries": beneficiaries
        }
    }

    monthly_expenses = {
        "housing": {
            "mortgage_or_rent": mortgage,
            "property_tax": property_tax,
            "repairs": household_repairs,
            "hoa_fees": hoa_fees
        },
        "transportation": {
            "car_payment": car_payment,
            "gas": gas,
            "maintenance": car_maintenance,
            "insurance": car_insurance
        },
        "food": {
            "groceries": groceries,
            "restaurants": restaurants,
            "pet_food": pet_food
        },
        "utilities": {
            "electricity": electricity,
            "water": water,
            "garbage": garbage,
            "phones": phones,
            "internet": internet
        },
        "healthcare": {
            "insurance": health_insurance,
            "other_medical": medical_expenses
        },
        "education_and_childcare": {
            "childcare": childcare
        },
        "entertainment": {
            "entertainment": entertainment,
            "subscriptions": subscriptions
        },
        "savings": {
            "general": savings,
            "retirement": retirement_savings
        }
    }

    report = {
        "user_profile": user_profile,
        "monthly_expenses": monthly_expenses,
        "retirement_forecast": retirement_forecast
    }
    report_json = json.dumps(report, indent=4)
    st.download_button("Download Budget, Retirement, and Estate Report (JSON)", report_json, file_name="personal_finance_report.json")
