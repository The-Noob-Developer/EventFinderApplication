import streamlit as st
import requests

st.title("🔐 Register New Account")

username = st.text_input("👤 Username")
email = st.text_input("📧 Email ID")
password = st.text_input("🔑 Password", type="password")

if st.button("Register"):
    if not username or not email or not password:
        st.warning("⚠️ All fields are mandatory.")
    else:
        try:
            response = requests.post(
                "https://eventfinderbackend.onrender.com/register",
                json={
                    "username": username,
                    "email": email,
                    "password": password
                }
            )

            if response.status_code == 200:
                st.success("🎉 Registration successful! You can now log in.")
                # Optional: redirect to login after success
                # st.experimental_rerun()  # or use st.switch_page("pages/login.py") if using multipage navigation
            else:
                # Try extracting error details
                try:
                    error_detail = response.json().get("detail", "")
                    if isinstance(error_detail, list) and "msg" in error_detail[0]:
                        st.error(error_detail[0]["msg"])
                    else:
                        st.error(f"❌ {error_detail}")
                except:
                    st.error("❌ Registration failed. Please try again.")

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Backend server is not reachable at https://eventfinderbackend.onrender.com.")
