import streamlit as st
import json
import os
from datetime import datetime
from backend.database import load_data

def show_call_history():
    st.header("📒 Communication History")

    # Show user-specific call history
    user_history = st.session_state.current_user.get("call_history", [])
    if user_history:
        st.subheader("Your Communication History")
        for call in reversed(user_history):
            with st.container():
                call_type = call.get('type', 'voice_call')
                if call_type == 'whatsapp':
                    st.markdown(f"**💬 WhatsApp Chat** - {call.get('timestamp', 'N/A')[:19].replace('T', ' ')}")
                    st.write(f"**Number:** {call.get('number', 'N/A')}")
                    st.write(f"**Assistant:** {call.get('assistant', 'N/A')}")
                    st.write(f"**Messages:** {len(call.get('messages', []))}")
                else:
                    st.markdown(f"**📞 Voice Call** - {call.get('timestamp', 'N/A')[:19].replace('T', ' ')}")
                    st.write(f"**Number:** {call.get('number', 'N/A')}")
                    st.write(f"**Assistant:** {call.get('assistant', 'N/A')}")
                    st.write(f"**Duration:** {call.get('duration', 'N/A')}")

                if call.get('messages'):
                    with st.expander("View Messages"):
                        for msg in call['messages']:
                            timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M:%S')
                            sender = "You" if msg['sender'] == 'user' else "AI"
                            st.write(f"**{sender}** ({timestamp}): {msg['message']}")
                st.divider()

    # Show call summaries from call_Summary.json
    summary_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "call_Summary.json")
    call_summaries = []
    if os.path.exists(summary_file):
        try:
            with open(summary_file, "r") as f:
                call_summaries = json.load(f)
        except Exception:
            call_summaries = []
    if call_summaries:
        st.subheader("Detailed Summaries (from Webhook)")
        for summary in reversed(call_summaries):
            with st.container():
                summary_type = summary.get('type', 'voice_call')
                icon = "💬" if summary_type == 'whatsapp' else "📞"
                st.markdown(f"{icon} **{summary_type.replace('_', ' ').title()}** - {summary.get('timestamp', 'N/A')[:19].replace('T', ' ')}")
                st.write(f"**Summary:** {summary.get('summary', 'N/A')}")
                st.write(f"**Phone:** {summary.get('user_phone', 'N/A')}")
                st.write(f"**Duration:** {summary.get('duration', 'N/A')}")
                if summary_type == 'whatsapp':
                    st.write(f"**Messages:** {summary.get('messages_count', 'N/A')}")
                with st.expander("Show Details"):
                    st.write(f"**Conversation ID:** {summary.get('conversation_id', 'N/A')}")
                    st.write(f"**Assistant ID:** {summary.get('assistant_id', 'N/A')}")
                    st.write(f"**Status:** {summary.get('status', 'N/A')}")
                    st.json(summary.get('raw', {}))
                st.divider()
    else:
        st.info("No communication summaries yet. Make some calls or WhatsApp chats to see them here.")

    if st.button("Clear All History", type="secondary"):
        users = load_data("users.json")
        user_id = st.session_state.current_user["id"]
        users[user_id]["call_history"] = []
        save_data(users, "users.json")
        st.session_state.current_user = users[user_id]
        st.success("Communication history cleared!")
        st.rerun()