import streamlit as st
from .components import auth, dashboard, voice_studio, assistants, calling, whatsapp, history

def main():
    st.set_page_config(
        page_title="AI Voice Changer with Vapi & Twilio",
        page_icon="🎭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    if 'selected_effect' not in st.session_state:
        st.session_state.selected_effect = None
    if 'calling' not in st.session_state:
        st.session_state.calling = False
    if 'dialed_number' not in st.session_state:
        st.session_state.dialed_number = ""
    if 'show_api_config' not in st.session_state:
        st.session_state.show_api_config = False
    if 'vapi_api_key' not in st.session_state:
        st.session_state.vapi_api_key = ""
    if 'twilio_account_sid' not in st.session_state:
        st.session_state.twilio_account_sid = ""
    if 'twilio_auth_token' not in st.session_state:
        st.session_state.twilio_auth_token = ""
    if 'twilio_phone_number' not in st.session_state:
        st.session_state.twilio_phone_number = ""
    if 'whatsapp_business_number' not in st.session_state:
        st.session_state.whatsapp_business_number = ""
    if 'voices_loaded' not in st.session_state:
        st.session_state.voices_loaded = False
    if 'call_text' not in st.session_state:
        st.session_state.call_text = "Hello, this is an AI generated voice call."
    if 'using_sample_voices' not in st.session_state:
        st.session_state.using_sample_voices = False
    if 'show_assistant_creation' not in st.session_state:
        st.session_state.show_assistant_creation = False
    if 'selected_assistant' not in st.session_state:
        st.session_state.selected_assistant = None
    
    # App header
    st.title("🎭 AI Voice Assistant with Vapi")
    st.markdown("### Create AI assistants that can have natural conversations over the phone")
    
    if st.session_state.authenticated:
        dashboard.show_dashboard()
    else:
        if st.session_state.show_signup:
            auth.show_signup_form()
        else:
            auth.show_login_form()

if __name__ == "__main__":
    main()