from tinydb import TinyDB, Query
from datetime import datetime
import streamlit as st

db = TinyDB("expense_tracker.json")  # This creates a JSON database file in the current directory
users_db = db.table("users")  # Create or access the 'users' table

# Test database setup (optional)
if st.button("Test Database"):
    users_db.insert({"email": "test@example.com", "password": "test123"})
    st.write("Test user added!")
    st.write(users_db.all())  # Display all records in the 'users' table