import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Agentic Commerce Chatbot", page_icon="🛒")

st.title("🛒 Agentic Commerce Chatbot")

# -----------------------------------
# Session State Initialization
# -----------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------------
# Display Chat History
# -----------------------------------
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# -----------------------------------
# User Input
# -----------------------------------
user_input = st.chat_input("Type your message...")

if user_input:

    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    try:
        payload = {
            "message": user_input,
        }

        # Pass session_id if exists
        if st.session_state.session_id:
            payload["session_id"] = st.session_state.session_id

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            data = response.json()

            # Store session_id
            st.session_state.session_id = data["session_id"]

            bot_reply = data["response"]

        else:
            bot_reply = "⚠️ Server error. Please try again."

    except Exception as e:
        bot_reply = f"⚠️ Could not connect to backend.\n\n{str(e)}"

    # Show bot message
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.chat_history.append(("assistant", bot_reply))
