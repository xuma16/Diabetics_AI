import streamlit as st
import pickle
import os
def show():
    # ---------------- Page Config ----------------
    st.set_page_config(
        page_title="Diabetes AI Chatbot",
        page_icon="🩺",
        layout="wide"
    )

    st.title("🤖 Diabetes AI Chatbot")

    # ---------------- Debug Section (IMPORTANT) ----------------
    st.subheader("🔍 Debug Info")

    model_path = "model.pkl"
    vectorizer_path = "vectorizer.pkl"

    # ---------------- Load Model Safely ----------------
    try:
        if not os.path.exists(model_path) or os.path.getsize(model_path) == 0:
            raise ValueError("model.pkl is missing or empty")

        if not os.path.exists(vectorizer_path) or os.path.getsize(vectorizer_path) == 0:
            raise ValueError("vectorizer.pkl is missing or empty")

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        with open(vectorizer_path, "rb") as f:
            vectorizer = pickle.load(f)

        st.success()

    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()

    # ---------------- App Description ----------------
    st.write(
        "Ask about diabetes in English or Swahili (Symptoms, Prevention, Treatment, Causes)\n"
        "Uliza kuhusu kisukari kwa Kiingereza au Kiswahili (Dalili, Kinga, Tiba, Sababu)"
    )

    # ---------------- Session State ----------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ---------------- User Input ----------------
    user_input = st.text_input("Type your question here / Andika swali lako hapa:")

    # ---------------- Prediction ----------------
    if st.button("Send / Tuma"):
        if user_input.strip() != "":
            try:
                X_input = vectorizer.transform([user_input])
                response = model.predict(X_input)[0]

                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": response
                })

            except Exception as e:
                st.error(f"Prediction error: {e}")
        else:
            st.warning("Please enter a question / Tafadhali andika swali")

    # ---------------- Chat Display ----------------
    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")
        st.markdown("---")

    # ---------------- Disclaimer ----------------
    st.write("⚠️ This app is for educational purposes only. Consult a doctor for medical advice.")
    st.write("⚠️ Programu hii ni kwa elimu tu. Tafadhali wasiliana na daktari kwa ushauri wa matibabu.")