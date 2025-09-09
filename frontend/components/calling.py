import streamlit as st
from datetime import datetime
from backend import database, vapi_integration

def show_make_call(twilio_configured):
    st.header("📞 Make AI Assistant Call")
    
    # Check if user has assistants
    user_assistants = st.session_state.current_user.get("assistants", [])
    if not user_assistants:
        st.error("You need to create an AI assistant first. Go to the 'AI Assistants' section.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Call Settings")
        
        # Assistant selection
        assistant_options = {f"{a.get('name', 'Unnamed Assistant')}": a for a in user_assistants}
        selected_assistant_name = st.selectbox("Select AI Assistant", options=list(assistant_options.keys()))
        selected_assistant = assistant_options[selected_assistant_name]
        st.session_state.selected_assistant = selected_assistant
        
        st.info(f"**Selected Assistant:** {selected_assistant.get('name', 'Unnamed Assistant')}")
        st.info(f"**Voice:** {selected_assistant.get('voice', {}).get('voiceId', 'N/A')}")
        st.info(f"**First Message:** {selected_assistant.get('firstMessage', 'N/A')}")
        
        # Phone number input
        phone_number = st.text_input("Phone Number to Call", 
                                   placeholder="+1234567890",
                                   value=st.session_state.dialed_number)
        
    with col2:
        st.subheader("Call Controls")
        
        if st.session_state.calling:
            st.success(f"📞 Calling {phone_number} with {selected_assistant.get('name', 'AI Assistant')}...")
            
            if 'call_start_time' not in st.session_state:
                st.session_state.call_start_time = datetime.now()
            
            call_duration = datetime.now() - st.session_state.call_start_time
            st.metric("Call Duration", f"{call_duration.seconds // 60}:{call_duration.seconds % 60:02d}")
            
            if st.button("📵 End Call", type="primary"):
                st.session_state.calling = False
                st.success("Call ended!")
                # Add to call history
                call_data = {
                    "timestamp": datetime.now().isoformat(),
                    "number": phone_number,
                    "duration": f"{call_duration.seconds} seconds",
                    "assistant": selected_assistant.get('name', 'Unnamed Assistant'),
                    "assistant_id": selected_assistant.get('id', 'N/A')
                }
                database.add_to_call_history(st.session_state.current_user["id"], call_data)
                database.save_call_history({
                    "caller_id": st.session_state.current_user["id"],
                    "receiver_id": selected_assistant.get('id'),
                    "timestamp": datetime.now().isoformat(),
                    "duration": f"{call_duration.seconds} seconds",
                    "status": "completed"
                })
                st.rerun()
        else:
            st.info("Ready to make an AI assistant call")
            
            if st.button("📞 Start AI Call", type="primary"):
                if not phone_number:
                    st.error("Please enter a phone number")
                    return
                
                # Make the call using Vapi
                if st.session_state.vapi_api_key:
                    vapi_ai = vapi_integration.VapiAI()
                    vapi_ai.setup_api_key(st.session_state.vapi_api_key)
                    
                    success, message = vapi_ai.make_call(
                        selected_assistant.get('id'),
                        phone_number
                    )
                    
                    if success:
                        st.session_state.calling = True
                        st.session_state.call_start_time = datetime.now()
                        st.session_state.dialed_number = phone_number
                        st.success("AI assistant call initiated!")
                        st.info(message)
                        st.rerun()
                    else:
                        st.error(f"Call failed: {message}")
                else:
                    # Demo mode
                    st.session_state.calling = True
                    st.session_state.call_start_time = datetime.now()
                    st.session_state.dialed_number = phone_number
                    st.success("AI assistant call initiated! (Demo Mode)")
                    st.info("In a real implementation, this would connect via Vapi")
                    st.rerun()