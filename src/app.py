import os

import streamlit as st
from dotenv import load_dotenv
from main_page import main_page
from view_selections_page import view_selections_page

load_dotenv()

st.set_page_config(layout="wide", page_title="Reale vs Synthetische Konversationen", page_icon="🤖")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main", "View Selections"])

# Add a password input for accessing the hidden page
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if page == "View Selections":
    if not st.session_state.authenticated:
        password = st.text_input("Enter password", type="password")
        if password == os.getenv("ADMIN_PW"):  # Replace with your actual password
            st.session_state.authenticated = True
            st.success("Authentication successful")
        else:
            st.error("Invalid password")
    else:
        view_selections_page()
else:
    main_page()
