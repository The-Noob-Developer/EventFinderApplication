import streamlit as st
import requests

st.title("🔐 Login Page for Registered Users")

username = st.text_input("👤 Username")
password = st.text_input("🔑 Password", type="password")

if st.button("Login"):
    if not username or not password:
        st.warning("⚠️ Both username and password are required.")
    else:
        try:
            response = requests.post(
                "https://eventfinderapplicationbackend.onrender.com/login",
                data={
                    "username": username,
                    "password": password
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response.raise_for_status()
            if response.status_code == 200:
                token = response.json().get("access_token")
                st.success("✅ Login successful")
                st.session_state.token = token
                st.session_state.logged_in = True
                # 🔄 Navigate to event page
                st.switch_page("pages/events.py")  # <-- update if filename is different
            else:
                st.error("❌ Login failed: Invalid credentials")
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Backend server is not reachable at https://eventfinderapplicationbackend.onrender.com")

# Optional: direct link to register
st.markdown("Don't have an account? [Register here](/register)")
