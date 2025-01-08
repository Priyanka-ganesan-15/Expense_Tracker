from tinydb import TinyDB, Query
from datetime import datetime
import streamlit as st

db = TinyDB("expense_tracker.json")  # This creates a JSON database file in the current directory
users_db = db.table("users")  # Create or access the 'users' table

# # Test database setup 
# if st.button("Test Database"):
#     users_db.insert({"email": "test@example.com", "password": "test123"})
#     st.write("Test user added!")
#     st.write(users_db.all())  # Display all records in the 'users' table

# Function to register a new user

def register_user(email, password):
    #check if user already exists 
    User = Query()
    if users_db.search(User.email == email):
        return False, "user already exists"
    
    #Add user to Database 
    users_db.insert({
        "email": email,
        "password": password,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return True, "User Registration Successful"

#UI Implementation for User Registration 

st.title("Expense Tracker - Register")
reg_email = st.text_input("Email")
reg_password = st.text_input("Password", type="password")

if st.button("Register"):
    if reg_email and reg_password:
        success, message = register_user(reg_email, reg_password)
        if success:
            st.success(message)
        else:
            st.error(message)
    else:
        st.error("Please fill in all fields.")

    