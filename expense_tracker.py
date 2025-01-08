from tinydb import TinyDB, Query
from datetime import datetime
import pandas as pd
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
    st.title("Expense Tracker")
    st.write("Welcome to the Expense Tracker! Manage your expenses effortlessly with real-time insights.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register"):
            st.session_state["page"] = "register"
    with col2:
        if st.button("Login"):
            st.session_state["page"] = "login"

elif st.session_state["page"] == "register":
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
    st.subheader("Login")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if login_email and login_password:
            status, user = authenticate_user(login_email, login_password)
            if status == "authenticated":
                st.session_state["user"] = user
                st.success(f"Welcome back, {login_email}!")
                st.session_state["page"] = "dashboard"
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
    st.title("Dashboard")
    st.write(f"Welcome, {st.session_state['user']['email']}!")

    # Add Expense Section
    st.subheader("Add Expense")
    expense_date = st.date_input("Date", datetime.now())
    expense_category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Other"])
    expense_amount = st.number_input("Amount", min_value=0.01, step=0.01)
    expense_description = st.text_input("Description (optional)")

    if st.button("Add Expense"):
        if expense_amount > 0:
            user_id = st.session_state["user"]["email"]
            db.table(user_id).insert({
                "date": expense_date.strftime("%Y-%m-%d"),
                "category": expense_category,
                "amount": expense_amount,
                "description": expense_description
            })
            st.success("Expense added successfully!")
        else:
            st.error("Please enter a valid amount.")

    # View Expenses Section
    st.subheader("View Expenses")
    user_id = st.session_state["user"]["email"]
    expenses = db.table(user_id).all()

    if expenses:
        df = pd.DataFrame(expenses).fillna("N/A")  # Ensure consistency
        st.dataframe(df)
    else:
        st.write("No expenses recorded yet.")

    # Expense Analysis Section
    st.subheader("Expense Analysis")
    if expenses:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        
        category_summary = df.groupby("category")["amount"].sum().reset_index()
        st.bar_chart(category_summary.set_index("category"))

        time_summary = df.groupby("date")["amount"].sum().reset_index()
        st.line_chart(time_summary.set_index("date"))

    # Logout Button
    if st.button("Logout"):
        st.session_state["page"] = "landing"
        st.session_state.pop("user", None)
