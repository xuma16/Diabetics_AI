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

    st.markdown(
        """
        <style>
            /* Hide Streamlit default footer and menu */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

            h1 {
                text-align: center;
                color: brown;
            }
            .center {
                text-align: center;
                color: brown;
            }

            /* ---- WhatsApp-style input bar ---- */
            .input-bar-wrapper {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: #f0f0f0;
                padding: 10px 16px;
                display: flex;
                align-items: center;
                gap: 10px;
                box-shadow: 0 -2px 8px rgba(0,0,0,0.15);
                z-index: 9999;
            }

            .input-bar-wrapper input[type="text"] {
                flex: 1;
                border: none;
                border-radius: 24px;
                padding: 12px 18px;
                font-size: 15px;
                background-color: #ffffff;
                outline: none;
                box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
            }

            .input-bar-wrapper button {
                background-color: #25D366;
                color: white;
                border: none;
                border-radius: 50%;
                width: 48px;
                height: 48px;
                font-size: 20px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                transition: background-color 0.2s;
            }

            .input-bar-wrapper button:hover {
                background-color: #1ebe5d;
            }

            /* Add bottom padding so chat history isn't hidden behind the fixed bar */
            .main .block-container {
                padding-bottom: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<h1>🩺 Diabetes AI Chatbot</h1>'
        '<div class="center">Ask me about diabetes &nbsp;|&nbsp; Niulize kuhusu kisukari</div>',
        unsafe_allow_html=True
    )

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

    # ---------------- Session State ----------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ---------------- WhatsApp-style Input Bar (using columns) ----------------
    col1, col2 = st.columns([9, 1])

    with col1:
        user_input = st.text_input(
            label="",
            placeholder="Type your question... / Andika swali lako...",
            key="user_input",
            label_visibility="collapsed"
        )

    with col2:
        send_clicked = st.button("➤", use_container_width=True)

    # Inject CSS to style the columns to look like a WhatsApp bar
    st.markdown(
        """
        <style>
            /* Target the two columns that form the input bar */
            div[data-testid="column"]:nth-of-type(1) input {
                border-radius: 24px 0 0 24px !important;
                border: 1.5px solid #ccc !important;
                padding: 12px 18px !important;
                font-size: 15px !important;
                background-color: #ffffff !important;
                height: 48px !important;
            }

            div[data-testid="column"]:nth-of-type(2) button {
                background-color: #25D366 !important;
                color: white !important;
                border-radius: 0 24px 24px 0 !important;
                border: none !important;
                height: 48px !important;
                font-size: 20px !important;
                font-weight: bold;
            }

            div[data-testid="column"]:nth-of-type(2) button:hover {
                background-color: #1ebe5d !important;
            }

            /* Remove top label gap */
            div[data-testid="column"] .stTextInput {
                margin-bottom: 0 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------------- Handle Send ----------------
    if send_clicked:
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
            st.warning("Please enter a question / Tafadhali andika swali")

    # ---------------- Chat Display (Newest on Top) ----------------
    st.markdown("### 💬 Chat History")

    for chat in reversed(st.session_state.chat_history):
        # User bubble (right side)
        st.markdown(
            f"""
            <div style="display:flex; justify-content:flex-end; margin-bottom:8px;">
                <div style="
                    background-color:#dcf8c6;
                    padding:10px 14px;
                    border-radius:16px 16px 4px 16px;
                    text-align:right;
                    display:inline-block;
                    max-width:70%;
                    word-wrap:break-word;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                ">
                    🧑 <b>You</b> <span style="font-size:10px;color:gray;">[{chat['time']}]</span><br>
                    {chat['user']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Bot bubble (left side)
        st.markdown(
            f"""
            <div style="display:flex; justify-content:flex-start; margin-bottom:8px;">
                <div style="
                    background-color:#ffffff;
                    padding:10px 14px;
                    border-radius:16px 16px 16px 4px;
                    display:inline-block;
                    max-width:70%;
                    word-wrap:break-word;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                    border: 1px solid #e0e0e0;
                ">
                    🤖 <b>Bot</b> <span style="font-size:10px;color:gray;">[{chat['time']}]</span><br>
                    {chat['bot']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------- Disclaimer ----------------
    st.markdown(
        '<div class="center" style="margin-top:20px;">⚠️ For education only. Consult a doctor.</div>',
        unsafe_allow_html=True
    )
