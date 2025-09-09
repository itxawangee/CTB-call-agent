import streamlit as st
from backend import vapi_integration, database
from backend.models import get_sample_voices

def show_ai_assistants():
    st.header("🤖 AI Assistants")
    
    if not st.session_state.vapi_api_key:
        st.error("Vapi API not configured. Please configure it in API Settings.")
        return
    
    # Create new assistant button
    if st.button("➕ Create New Assistant"):
        st.session_state.show_assistant_creation = True
        st.rerun()
    
    if st.session_state.show_assistant_creation:
        show_create_assistant()
        return
    
    # List user's assistants
    user_assistants = st.session_state.current_user.get("assistants", [])
    if user_assistants:
        st.subheader("Your AI Assistants")
        for assistant in user_assistants:
            with st.expander(f"{assistant.get('name', 'Unnamed Assistant')}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**ID:** {assistant.get('id', 'N/A')}")
                    st.write(f"**First Message:** {assistant.get('firstMessage', 'N/A')}")
                    st.write(f"**Model:** {assistant.get('model', {}).get('model', 'N/A') if isinstance(assistant.get('model'), dict) else assistant.get('model', 'N/A')}")
                    st.write(f"**Voice:** {assistant.get('voice', {}).get('voiceId', 'N/A') if isinstance(assistant.get('voice'), dict) else assistant.get('voice', 'N/A')}")
                with col2:
                    st.write(f"**Created:** {assistant.get('createdAt', 'N/A')}")
                st.divider()
    else:
        st.info("No assistants found. Click 'Create New Assistant' to get started.")
    
    # Load assistants from Vapi
    if st.button("🔄 Load Assistants from Vapi"):
        with st.spinner("Loading assistants from Vapi API..."):
            vapi_ai = vapi_integration.VapiAI()
            vapi_ai.setup_api_key(st.session_state.vapi_api_key)
            assistants = vapi_ai.get_assistants()
            if assistants:
                st.success(f"Loaded {len(assistants)} assistants from Vapi!")
                # Store in user data
                for assistant in assistants:
                    database.save_user_assistant(st.session_state.current_user["id"], assistant)
                st.session_state.current_user["assistants"] = assistants
                st.rerun()
            else:
                st.error("Failed to load assistants from Vapi API")

def show_create_assistant():
    st.header("🆕 Create AI Assistant")

    if not st.session_state.vapi_api_key:
        st.error("Vapi API not configured. Please configure it in API Settings.")
        return

    with st.form("create_assistant_form"):
        st.subheader("Assistant Details")

        # Assistant name
        name = st.text_input("Assistant Name", placeholder="My AI Assistant")

        # Voice selection
        voices = get_sample_voices()
        if voices:
            voice_options = {f"{v['name']} ({v.get('category', 'custom')})": v['voice_id'] for v in voices}
            selected_voice_name = st.selectbox("Select Voice", options=list(voice_options.keys()))
            voice_id = voice_options[selected_voice_name]
        else:
            st.error("No voices available. Please configure ElevenLabs API.")
            return

        # Model selection
        model_options = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
        selected_model = st.selectbox("Select AI Model", options=model_options, index=0)

        # System instructions/prompt
        prompt = st.text_area("System Instructions", height=150,
                            placeholder="You are a helpful AI assistant...",
                            value="You are a helpful, friendly AI assistant. Answer questions clearly and concisely.")

        # First message for the assistant
        first_message = st.text_input("First Message",
                                   placeholder="Hello! How can I assist you today?",
                                   value="Hello! Thank you for contacting me. How can I help you today?")

        col1, col2 = st.columns(2)
        with col1:
            create_button = st.form_submit_button("Create Assistant", type="primary")
        with col2:
            cancel_button = st.form_submit_button("Cancel")

        if create_button:
            if not all([name, first_message, prompt]):
                st.error("Please fill in all required fields")
                return

            with st.spinner("Creating assistant via Vapi API..."):
                vapi_ai = vapi_integration.VapiAI()
                vapi_ai.setup_api_key(st.session_state.vapi_api_key)
                
                # Create assistant using VapiAI class
                assistant = vapi_ai.create_assistant(
                    name=name,
                    voice_id=voice_id,
                    first_message=first_message,
                    model=selected_model,
                    instructions=prompt
                )

                if assistant:
                    # Save to user data
                    database.save_user_assistant(st.session_state.current_user["id"], assistant)
                    st.session_state.current_user["assistants"] = st.session_state.current_user.get("assistants", []) + [assistant]
                    st.success("Assistant created successfully!")
                    st.session_state.show_assistant_creation = False
                    st.rerun()
                else:
                    st.error("Error creating assistant. Please check your API configuration.")

        if cancel_button:
            st.session_state.show_assistant_creation = False
            st.rerun()