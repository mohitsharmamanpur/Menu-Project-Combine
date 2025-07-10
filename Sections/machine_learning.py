import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

def machine_learning_section():
    st.header("🧠 Machine Learning Models")
    ml_model = st.selectbox("Select ML Model", [
        "Machine Learning Model-1",
        "Machine Learning Model-2",
        "Machine Learning Model-3",
        "Machine Learning Model-4",
        "Machine Learning Model-5"
    ])
    if ml_model == "Machine Learning Model-1":
        st.subheader("Salary Prediction using Linear Regression")
        try:
            dataset = pd.read_csv("Salary-data.csv")
            x = dataset["YearsExperience"].values.reshape(-1, 1)
            y = dataset["Salary"].values.reshape(-1, 1)
            model = LinearRegression()
            model.fit(x, y)
            years_exp = st.number_input("Enter Years of Experience:", min_value=0.0, max_value=50.0, step=0.1)
            if st.button("Predict Salary"):
                prediction = model.predict([[years_exp]])
                st.success(f"Predicted Salary for {years_exp} years experience: ₹ {prediction[0][0]:,.2f}")
                st.info(f"Slope (coefficient): {model.coef_[0][0]:.2f}")
                st.info(f"Intercept (bias): {model.intercept_[0]:.2f}")
        except Exception as e:
            st.error(f"Error: {e}")

    elif ml_model == "Machine Learning Model-2":
        st.subheader("Startup Profit Prediction using Multiple Linear Regression")
        try:
            dataset = pd.read_csv("50startups.csv")
            dataset = pd.get_dummies(dataset, columns=['State'], drop_first=True)
            x = dataset[['R&D Spend', 'Administration', 'Marketing Spend', 'State_Florida', 'State_New York']]
            y = dataset['Profit']
            model = LinearRegression()
            model.fit(x, y)
            st.markdown("### Enter Startup Investment Details")
            rd_spend = st.number_input("R&D Spend (₹)", min_value=0.0, step=1000.0, format="%.2f")
            admin = st.number_input("Administration Spend (₹)", min_value=0.0, step=1000.0, format="%.2f")
            marketing = st.number_input("Marketing Spend (₹)", min_value=0.0, step=1000.0, format="%.2f")
            state = st.selectbox("State", ["California", "Florida", "New York"])
            state_florida = 1 if state == "Florida" else 0
            state_newyork = 1 if state == "New York" else 0
            if st.button("Predict Profit"):
                input_data = [[rd_spend, admin, marketing, state_florida, state_newyork]]
                prediction = model.predict(input_data)
                st.success(f"Predicted Profit: ₹ {prediction[0]:,.2f}")
                st.info(f"Slope (coefficients): {model.coef_}")
                st.info(f"Intercept (bias): {model.intercept_:.2f}")
        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.info(f"{ml_model} is under construction 🚧.")
