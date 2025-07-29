
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
data = pd.read_csv('credit_data.csv')

# Target and features
X = data.drop(columns=['SeriousDlqin2yrs'])
y = data['SeriousDlqin2yrs']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Streamlit UI
st.title("🏦 Credit Risk Prediction App")

st.sidebar.header("Enter Customer Details")

# Collect user input
age = st.sidebar.slider("Age", 18, 70, 30)
monthly_income = st.sidebar.number_input("Monthly Income (INR)", value=10000)
debt_ratio = st.sidebar.slider("Debt Ratio", 0.0, 2.0, 0.5)
revolving_utilization = st.sidebar.slider("Revolving Utilization", 0.0, 1.0, 0.5)
num_dependents = st.sidebar.number_input("Number of Dependents", value=1, step=1)
num_open_credit = st.sidebar.number_input("Open Credit Lines and Loans", value=5, step=1)
num_real_estate_loans = st.sidebar.number_input("Real Estate Loans", value=1, step=1)
num_30_59 = st.sidebar.slider("30-59 Days Past Due", 0, 10, 0)
num_60_89 = st.sidebar.slider("60-89 Days Past Due", 0, 10, 0)
num_90_late = st.sidebar.slider("90+ Days Late", 0, 10, 0)

# Predict
input_data = pd.DataFrame([[revolving_utilization, age, num_30_59, debt_ratio, monthly_income,
                            num_open_credit, num_90_late, num_real_estate_loans,
                            num_60_89, num_dependents]],
                          columns=X.columns)

input_scaled = scaler.transform(input_data)
prediction = model.predict(input_scaled)[0]
probability = model.predict_proba(input_scaled)[0][1]

# Output
if prediction == 1:
    st.error(f"❌ High Credit Risk\nProbability of Default: {probability:.2f}")
else:
    st.success(f"✅ Low Credit Risk\nProbability of Default: {probability:.2f}")
