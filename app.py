import streamlit as st
import AskAboutDiabets, MeasureYourDiabets

page = st.sidebar.selectbox(
    "Navigate",
    ["Home","Dashboard","Analysis"]
)

if page == "home":
    AskAboutDiabets.show()
elif page == "Dashboard":
    MeasureYourDiabets.show()
