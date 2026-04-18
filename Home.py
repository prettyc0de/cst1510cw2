import streamlit as st
from hashing import generate_hash, is_valid_hash
from app_model.db import get_connection
from app_model.users import add_user,get_user


conn = get_connection()

st.set_page_config(
    page_title = "Home",
    page_icon = "🏠",
    layout = "wide"
)

st.title("Welcome to the Multi-Domain Intelligence Platform 🏠")
st.write("Please register or log in to access the Cybersecurity Dashboard and AI Assistant.")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

tab_login, tab_register = st.tabs(["Login Status", "Register"])

with tab_login:
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")


    if st.button("Log In"):
        user = get_user(conn, login_username)

        if user is None:
            st.error("Username not found.")
        else:
            user_id, user_name, user_hash = user

            if login_username == user_name and is_valid_hash(login_password, user_hash):
                st.session_state["logged_in"] = True
                st.session_state["username"] = user_name
                st.success("Logged in successfully! Please open a dashboard from the sidebar.")
            else:
                st.error("Invalid password.")

with tab_register:
    register_username = st.text_input("New Username")
    register_password = st.text_input("New Password", type="password")

    if st.button("Register"):
        if register_username.strip() == "" or register_password.strip() == "":
            st.warning("Please enter both username and password.")
        else:
            hash_password = generate_hash(register_password)
            add_user(conn, register_username, hash_password)
            st.success("Registration successful! Please log in.")

st.write("Current Login Status:", st.session_state["logged_in"])