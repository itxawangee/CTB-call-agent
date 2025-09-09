import streamlit as st
import os
from backend import database, vapi_integration, twilio_integration

# Initialize APIs
vapi_ai = vapi_integration.VapiAI()

def init_databases():
    database.init_db("users.json")
    database.init_call_history_db("call_history.json")

def setup_apis():
    vapi_ai.setup_api_key()
    twilio_configured, twilio_message = twilio_integration.setup_twilio_integration()
    return twilio_configured