import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    st.stop()

st.title("Cybersecurity AI Assistant 🤖")
st.write("Ask the AI assistant for help understanding cyber incidents, phishing trends, and response actions.")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not set. Please add it to your environment variables.")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a beginner-friendly, intermediate level and advanced cybersecurity assistant depending on the situation. Reply in very simple English. Keep answers short, clear, and useful. Use 6 to 10 lines only unless the user asks for more detail. Focus only on cybersecurity topics such as phishing, incidents, dashboards, and response actions, Data Science topics and it operational topics."
        } 
]

for message in st.session_state.messages[1:]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("Ask a cybersecurity question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=st.session_state.messages
        )

        reply = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

    except Exception as e:
        st.error(f"Error: {e}")