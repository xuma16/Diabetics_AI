import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("diabetes_model.pkl", "rb"))

st.title("Diabetes Prediction AI")

preg = st.number_input("Pregnancies")
glucose = st.number_input("Glucose Level")
bp = st.number_input("Blood Pressure")
skin = st.number_input("Skin Thickness")
insulin = st.number_input("Insulin")
bmi = st.number_input("BMI")
age = st.number_input("Age")

if st.button("Predict"):
    data = np.array([[preg, glucose, bp, skin, insulin, bmi, age]])
    prediction = model.predict(data)

    if prediction[0] == 1:
        st.error("⚠️ The person is Diabetic")
    else:
        st.success("✅ The person is Not Diabetic")
