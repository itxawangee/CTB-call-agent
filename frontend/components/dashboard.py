import streamlit as st
from backend import twilio_integration
from . import voice_studio, assistants, calling, whatsapp, history
from ..utils import setup_apis

def show_dashboard():
    # Sidebar user info
    st.sidebar.success(f"Welcome, {st.session_state.current_user['username']}!")
    
    # API Configuration button
    if st.sidebar.button("⚙️ API Configuration"):
        st.session_state.show_api_config = True
        st.rerun()
    
    if st.session_state.show_api_config:
        show_api_configuration()
        return
    
    # Setup integrations
    twilio_configured, twilio_message = twilio_integration.setup_twilio_integration()
    vapi_configured = st.session_state.vapi_api_key is not None
    
    # Show API status
    with st.sidebar.expander("API Status"):
        st.write(f"**Vapi:** {'✅ Configured' if vapi_configured else '❌ Not Configured'}")
        st.write(f"**Twilio:** {'✅ Configured' if twilio_configured else '❌ Not Configured'}")
        whatsapp_configured = bool(st.session_state.whatsapp_business_number)
        st.write(f"**WhatsApp:** {'✅ Configured' if whatsapp_configured else '❌ Not Configured'}")
        if st.session_state.using_sample_voices:
            st.warning("Using sample voices (API not available)")
        if not vapi_configured:
            st.error("Please configure Vapi API to use all features")
        if not whatsapp_configured:
            st.warning("Configure WhatsApp Business number for WhatsApp conversations")
    
    # Navigation
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Navigation")
    menu_options = ["Voice Studio", "AI Assistants", "Make Call", "WhatsApp Chat", "Call History", "Account"]
    selected_menu = st.sidebar.radio("Go to", menu_options)
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.rerun()
    
    # Main content
    if selected_menu == "Voice Studio":
        voice_studio.show_voice_studio()
    elif selected_menu == "AI Assistants":
        assistants.show_ai_assistants()
    elif selected_menu == "Make Call":
        calling.show_make_call(twilio_configured)
    elif selected_menu == "WhatsApp Chat":
        whatsapp.show_whatsapp_chat()
    elif selected_menu == "Call History":
        history.show_call_history()
    elif selected_menu == "Account":
        show_account_info()

def show_api_configuration():
    st.header("⚙️ API Configuration")
    
    st.warning("API configuration is required for full functionality")
    
    with st.form("api_config_form"):
        st.subheader("Vapi API")
        st.info("Get your API key from https://vapi.ai")
        vapi_key = st.text_input("Vapi API Key", 
                                value=st.session_state.vapi_api_key,
                                type="password")
        
        st.subheader("Twilio API")
        st.info("Get credentials from https://twilio.com")
        twilio_sid = st.text_input("Twilio Account SID", 
                                  value=st.session_state.twilio_account_sid)
        twilio_token = st.text_input("Twilio Auth Token", 
                                    value=st.session_state.twilio_auth_token,
                                    type="password")
        twilio_phone = st.text_input("Twilio Phone Number",
                                     value=st.session_state.twilio_phone_number,
                                     placeholder="+1234567890")

        st.subheader("WhatsApp Business API (Twilio)")
        st.info("Configure Twilio WhatsApp for AI-powered WhatsApp conversations")
        whatsapp_business_number = st.text_input("Twilio WhatsApp Number",
                                               value=st.session_state.whatsapp_business_number,
                                               placeholder="+1234567890")
        st.info("Set webhook URL in Twilio: http://your-server:5000/whatsapp-webhook")
        
        col1, col2 = st.columns(2)
        with col1:
            save_button = st.form_submit_button("Save API Configuration", type="primary")
        with col2:
            cancel_button = st.form_submit_button("Cancel")
        
        if save_button:
            # Save to session state
            st.session_state.vapi_api_key = vapi_key
            st.session_state.twilio_account_sid = twilio_sid
            st.session_state.twilio_auth_token = twilio_token
            st.session_state.twilio_phone_number = twilio_phone
            st.session_state.whatsapp_business_number = whatsapp_business_number
            
            # Update APIs
            from ..utils import vapi_ai
            vapi_ai.setup_api_key(vapi_key)
            
            # Reload voices with real API
            if vapi_key:
                with st.spinner("Loading voices from API..."):
                    voices = vapi_ai.get_assistants()
                    if voices:
                        st.success(f"Loaded {len(voices)} voices from Vapi!")
                        st.session_state.using_sample_voices = False
                    else:
                        st.error("Failed to load voices from Vapi API")
                        st.session_state.using_sample_voices = True
            
            st.success("API configuration saved!")
            st.session_state.show_api_config = False
            st.rerun()
        
        if cancel_button:
            st.session_state.show_api_config = False
            st.rerun()

def show_account_info():
    st.header("👤 Account Information")
    
    user = st.session_state.current_user
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Username:** {user['username']}")
        st.info(f"**Email:** {user['email']}")
        st.info(f"**Member since:** {user['created_at'][:10]}")
    
    with col2:
        status = "Premium 🎯" if user['premium'] else "Free Tier"
        st.info(f"**Account Status:** {status}")
        
        if not user['premium']:
            st.markdown("---")
            st.subheader("Upgrade to Premium")
            st.markdown("""
            - 🎭 Unlimited AI voice generations
            - 🤖 Multiple AI assistants
            - 📞 Priority call processing
            - 🚫 No advertisements
            """)
            
            if st.button("Upgrade to Premium", type="primary"):
                from backend.database import load_data, save_data
                users = load_data("users.json")
                users[user['id']]['premium'] = True
                save_data(users, "users.json")
                st.session_state.current_user['premium'] = True
                st.success("Account upgraded to Premium!")
                st.rerun()