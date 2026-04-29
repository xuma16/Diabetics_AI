import streamlit as st
import pickle
import os
from datetime import datetime

def show():
    # ---------------- Page Config ----------------
    st.set_page_config(
        page_title="Diabetes AI Chatbot",
        page_icon="🩺",
        layout="wide"
    )

    st.title("🤖 Diabetes AI Chatbot")

    # ---------------- Load Model ----------------
    model_path = "model.pkl"
    vectorizer_path = "vectorizer.pkl"

    try:
        if not os.path.exists(model_path) or os.path.getsize(model_path) == 0:
            raise ValueError("model.pkl is missing or empty")

        if not os.path.exists(vectorizer_path) or os.path.getsize(vectorizer_path) == 0:
            raise ValueError("vectorizer.pkl is missing or empty")

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        with open(vectorizer_path, "rb") as f:
            vectorizer = pickle.load(f)

    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()

    # ---------------- Description ----------------
    st.write(
        "Ask about diabetes in English or Swahili\n"
        "Uliza kuhusu kisukari kwa Kiingereza au Kiswahili"
    )

    # ---------------- Session State ----------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ---------------- User Input ----------------
    user_input = st.text_input("Type your question here / Andika swali lako hapa:")

    if st.button("Send / Tuma"):
        if user_input.strip() != "":
            try:
                X_input = vectorizer.transform([user_input])
                response = model.predict(X_input)[0]

                timestamp = datetime.now().strftime("%H:%M:%S")

                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": response,
                    "time": timestamp
                })

            except Exception as e:
                st.error(f"Prediction error: {e}")
        else:
            st.warning("Please enter a question")

    # ---------------- Chat Display (Newest on Top) ----------------
    st.markdown("### 💬 Chat History")

    chat_container = st.container()

    with chat_container:
        for chat in reversed(st.session_state.chat_history):

            # User message
            st.markdown(
                f"""
                <div style="
                    background-color:#e6f2ff;
                    padding:10px;
                    border-radius:10px;
                    margin-bottom:5px;
                ">
                    🧑 <b>You</b> 
                    <span style="font-size:10px;color:gray;">[{chat['time']}]</span><br>
                    {chat['user']}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Bot message
            st.markdown(
                f"""
                <div style="
                    background-color:#f0f0f0;
                    padding:10px;
                    border-radius:10px;
                    margin-bottom:10px;
                ">
                    🤖 <b>Bot</b> 
                    <span style="font-size:10px;color:gray;">[{chat['time']}]</span><br>
                    {chat['bot']}
                </div>
                """,
                unsafe_allow_html=True
            )

    # ---------------- Auto Scroll to Top ----------------
    st.markdown(
        """
        <script>
            window.scrollTo({ top: 0, behavior: 'smooth' });
        </script>
        """,
        unsafe_allow_html=True
    )

    # ---------------- Disclaimer ----------------
    st.write("⚠️ For education only. Consult a doctor.")


# Run the app
if __name__ == "__main__":
    show()
