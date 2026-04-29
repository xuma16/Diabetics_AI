import streamlit as st
import AskAboutDiabets, MeasureYourDiabets

page = st.sidebar.selectbox(
    "Navigate",
    ["Ask About Diabets","Measure Your Diabets"]
)

if page == "Ask About Diabets":
    AskAboutDiabets.show()
elif page == "Measure Your Diabets":
    MeasureYourDiabets.show()
