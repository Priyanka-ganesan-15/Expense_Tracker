from tinydb import TinyDB, Query
from datetime import datetime
import streamlit as st

# Initialize database
db = TinyDB("expense_tracker.json")
users_db = db.table("users")  # Create or access the 'users' table

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state["page"] = "landing"

# Function to register a new user
def register_user(email, password):
    User = Query()
    if users_db.search(User.email == email):
        return False, "User already exists!"
    # Add user to the database
    users_db.insert({
        "email": email,
        "password": password,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return True, "User registration successful!"

# Function to authenticate a user
def authenticate_user(email, password):
    User = Query()
    user = users_db.search(User.email == email)
    if user:
        if user[0]["password"] == password:
            return "authenticated", user[0]
        else:
            return "incorrect_password", None
    return "user_not_found", None

# Navigation logic
if st.session_state["page"] == "landing":
    # Landing Page
    st.title("Expense Tracker")
    st.write("Welcome to the Expense Tracker! Manage your expenses effortlessly with real-time insights.")

    if st.button("Register"):
        st.session_state["page"] = "register"

    if st.button("Login"):
        st.session_state["page"] = "login"

elif st.session_state["page"] == "register":
    # Registration Page
    st.subheader("Register")
    reg_email = st.text_input("Email", key="reg_email")
    reg_password = st.text_input("Password", type="password", key="reg_password")

    if st.button("Register"):
        if reg_email and reg_password:
            success, message = register_user(reg_email, reg_password)
            if success:
                st.success(message)
                st.session_state["page"] = "login"
            else:
                st.error(message)
        else:
            st.error("Please fill in all fields.")

    if st.button("Back to Login"):
        st.session_state["page"] = "login"

elif st.session_state["page"] == "login":
    # Login Page
    st.subheader("Login")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if login_email and login_password:
            status, user = authenticate_user(login_email, login_password)
            if status == "authenticated":
                st.session_state["user"] = user
                st.success(f"Welcome back, {login_email}!")
                st.session_state["page"] = "dashboard"  # Redirect to dashboard
            elif status == "incorrect_password":
                st.error("Incorrect password.")
            elif status == "user_not_found":
                st.warning("User doesn't exist. Please register.")
                if st.button("Go to Register"):
                    st.session_state["page"] = "register"
        else:
            st.error("Please fill in all fields.")

    if st.button("Back to Register"):
        st.session_state["page"] = "register"

elif st.session_state["page"] == "dashboard":
    # Placeholder for Dashboard
    st.title("Dashboard")
    st.write("This is your expense tracking dashboard.")
    if st.button("Logout"):
        st.session_state["page"] = "landing"
        st.session_state.pop("user", None)
