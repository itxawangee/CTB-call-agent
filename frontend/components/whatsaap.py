import streamlit as st
import json
import os

def show_whatsapp_chat():
    st.header("💬 WhatsApp Chat with AI Assistant (Twilio + VAPI)")

    st.info("📱 **Twilio WhatsApp Integration:** Messages are processed through Twilio WhatsApp → VAPI AI → Response sent back via WhatsApp")

    # Check Twilio WhatsApp configuration
    whatsapp_configured = bool(st.session_state.whatsapp_business_number)
    if not whatsapp_configured:
        st.error("Please configure your Twilio WhatsApp number in API Configuration first.")
        return

    st.success(f"✅ **Twilio WhatsApp Configured:** {st.session_state.whatsapp_business_number}")
    st.info("🤖 **VAPI AI Integration:** All incoming WhatsApp messages are processed by VAPI AI")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📋 Setup Instructions")

        st.markdown("""
        ### To enable WhatsApp AI Chat:

        1. **Configure Twilio WhatsApp:**
           - Go to Twilio Console → WhatsApp
           - Connect your WhatsApp Business number
           - Set webhook URL: `http://your-server:5000/whatsapp-webhook`

        2. **Test the Integration:**
           - Send a WhatsApp message to your Twilio number
           - VAPI AI will automatically respond
           - Use keywords like "voice message" for audio responses

        3. **Voice Messages:**
           - Users can request voice replies by saying:
             - "voice message", "voice reply", "speak to me"
             - "voice response", "audio message", "voice note"
        """)

        if st.button("🔄 Refresh WhatsApp Logs"):
            st.rerun()

    with col2:
        st.subheader("📊 WhatsApp Activity Monitor")

        # Load and display recent WhatsApp conversations
        summary_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "call_Summary.json")

        whatsapp_messages = []
        if os.path.exists(summary_file):
            try:
                with open(summary_file, "r") as f:
                    all_summaries = json.load(f)
                    whatsapp_messages = [msg for msg in all_summaries if msg.get('type') == 'whatsapp']
            except Exception:
                whatsapp_messages = []

        if whatsapp_messages:
            st.success(f"📱 **Recent Activity:** {len(whatsapp_messages)} WhatsApp conversations")

            # Display recent messages
            for msg in reversed(whatsapp_messages[-5:]):  # Show last 5
                with st.expander(f"💬 {msg.get('from_number', 'Unknown')} - {msg.get('timestamp', 'N/A')[:19].replace('T', ' ')}"):
                    st.write(f"**User:** {msg.get('user_message', 'N/A')}")
                    st.write(f"**AI Response:** {msg.get('ai_response', 'N/A')}")
                    if msg.get('voice_requested'):
                        st.info(f"🎵 Voice requested: {msg.get('voice_generated', False)}")
                    st.divider()
        else:
            st.info("📭 No WhatsApp messages yet. Send a message to your Twilio WhatsApp number to see activity here.")

        # Quick stats
        total_messages = len(whatsapp_messages)
        voice_requests = sum(1 for msg in whatsapp_messages if msg.get('voice_requested', False))
        voice_generated = sum(1 for msg in whatsapp_messages if msg.get('voice_generated', False))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Messages", total_messages)
        with col2:
            st.metric("Voice Requests", voice_requests)
        with col3:
            st.metric("Voice Generated", voice_generated)