import requests
import os
import time

class VapiAI:
    def __init__(self):
        self.api_key = None
        
    def setup_api_key(self, api_key=None):
        if api_key:
            self.api_key = api_key
            return True
        
        env_api_key = os.getenv("VAPI_API_KEY")
        if env_api_key:
            self.api_key = env_api_key
            return True
            
        return False
    
    def create_assistant(self, name, voice_id, first_message, model, instructions):
        if not self.api_key:
            return None

        try:
            url = "https://api.vapi.ai/assistant"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "name": name,
                "firstMessage": first_message,
                "model": {
                    "provider": "openai",
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": instructions
                        }
                    ]
                },
                "voice": {
                    "provider": "11labs",
                    "voiceId": voice_id
                },
                "transcriber": {
                    "provider": "deepgram",
                    "model": "nova-2",
                    "language": "en-US"
                },
                "maxDurationSeconds": 600,
                "interruptionsEnabled": True
            }
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 201:
                return response.json()
            else:
                return None
        except Exception as e:
            return None

    def make_call(self, assistant_id, phone_number):
        if not self.api_key:
            return None, "API key not configured"
        
        try:
            url = "https://api.vapi.ai/call/phone"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "assistantId": assistant_id,
                "phoneNumber": {"number": phone_number}
            }
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 201:
                call_data = response.json()
                call_id = call_data.get("id")
                return call_data, None
            else:
                return None, f"API error: {response.status_code} - {response.text}"
        except Exception as e:
            return None, f"Error making call: {str(e)}"
    
    def get_assistants(self):
        if not self.api_key:
            return []
        
        try:
            url = "https://api.vapi.ai/assistant"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('assistants', [])
            else:
                return []
        except Exception as e:
            return []

    def get_voices(self):
        if not self.api_key:
            return []

        try:
            url = "https://api.vapi.ai/voices"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('voices', [])
            else:
                return []
        except Exception as e:
            return []

    def start_whatsapp_conversation(self, assistant_id, whatsapp_number):
        if not self.api_key:
            return None, "API key not configured"

        try:
            url = "https://api.vapi.ai/message"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "assistantId": assistant_id,
                "channel": {
                    "type": "whatsapp",
                    "number": whatsapp_number
                },
                "message": {
                    "type": "text",
                    "text": "Hello! I'm starting our conversation. How can I help you today?"
                }
            }
            response = requests.post(url, headers=headers, json=data, timeout=30)

            if response.status_code == 201:
                conversation_data = response.json()
                return conversation_data, None
            elif response.status_code == 404:
                return None, "WhatsApp not supported by VAPI."
            else:
                return None, f"API error: {response.status_code} - {response.text}"
        except Exception as e:
            return None, f"Error starting WhatsApp conversation: {str(e)}"

    def send_whatsapp_message(self, conversation_id, message):
        if not self.api_key:
            return None, "API key not configured"

        try:
            url = "https://api.vapi.ai/message"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "conversationId": conversation_id,
                "type": "whatsapp",
                "message": {
                    "type": "text",
                    "text": message
                }
            }
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json(), None
            else:
                return None, f"API error: {response.status_code} - {response.text}"
        except Exception as e:
            return None, f"Error sending WhatsApp message: {str(e)}"

    def get_conversation_history(self, conversation_id):
        if not self.api_key:
            return []

        try:
            url = f"https://api.vapi.ai/message?conversationId={conversation_id}"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('messages', [])
            else:
                return []
        except Exception as e:
            return []

    def end_whatsapp_conversation(self, conversation_id):
        if not self.api_key:
            return False, "API key not configured"

        try:
            url = f"https://api.vapi.ai/message/{conversation_id}/end"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, timeout=10)
            return response.status_code == 200, None
        except Exception as e:
            return False, f"Error ending conversation: {str(e)}"