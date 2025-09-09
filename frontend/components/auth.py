import streamlit as st
from backend.auth import register_user, authenticate_user

def show_login_form():
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.header("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            login_button = st.form_submit_button("Login")
        with col2:
            signup_button = st.form_submit_button("Create Account")
        
        if login_button:
            if username and password:
                success, result = authenticate_user(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.current_user = result
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.error("Please fill in all fields")
        
        if signup_button:
            st.session_state.show_signup = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_signup_form():
    st.markdown("""
    <style>
    .signup-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="signup-container">', unsafe_allow_html=True)
    st.header("Create Account")
    
    with st.form("signup_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Create password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
        
        terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            signup_button = st.form_submit_button("Sign Up")
        with col2:
            back_button = st.form_submit_button("Back to Login")
        
        if signup_button:
            if not all([username, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            elif not terms:
                st.error("Please agree to the terms and conditions")
            else:
                success, message = register_user(username, email, password)
                if success:
                    st.success(message)
                    st.session_state.show_signup = False
                    st.rerun()
                else:
                    st.error(message)
        
        if back_button:
            st.session_state.show_signup = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)