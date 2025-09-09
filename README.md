# 🎭 AI Voice Assistant with Vapi

A comprehensive **web application** that enables users to create AI assistants capable of having natural conversations over **phone calls** and **WhatsApp messages**.  
Built with **Streamlit**, powered by **Vapi.ai**, **Twilio**, and **ElevenLabs** integrations.

---

## ✨ Features

- 🤖 **AI Assistant Creation** – Custom assistants with unique voices and personalities  
- 📞 **Voice Calls** – Make AI-powered phone calls via Vapi  
- 💬 **WhatsApp Integration** – Conversational AI on WhatsApp using Twilio  
- 🎭 **Voice Studio** – Preview and test different AI voices  
- 📒 **Communication History** – Track calls, messages, and assistant logs  
- 👤 **User Accounts** – Secure authentication and profiles  
- ⚙️ **API Configuration** – Easy setup for Vapi, Twilio & ElevenLabs  

---

## 🚀 Getting Started

### ✅ Prerequisites
- Python **3.8+**  
- [Vapi.ai](https://vapi.ai) API key  
- [Twilio](https://www.twilio.com/) account (for WhatsApp integration)  
- [ElevenLabs](https://elevenlabs.io/) account (for voice generation)  

### 📥 Installation
---
Install dependencies:

```bash
pip install -r requirements.txt
```

Create a **.env** file in the root directory:

```env
VAPI_API_KEY=your_vapi_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
WHATSAPP_BUSINESS_NUMBER=your_whatsapp_business_number
```

Run the application:

```bash
streamlit run app.py
```

---

## 📋 Usage

### 1️⃣ User Authentication

* Create an account or login
* Passwords securely hashed with **bcrypt**

### 2️⃣ API Configuration

* Add **Vapi** and **Twilio** API keys in settings
* Set WhatsApp Business number

### 3️⃣ Creating AI Assistants

* Define assistant **name** and **personality**
* Choose AI models (GPT-4, GPT-3.5-turbo, etc.)
* Select custom voice and system instructions

### 4️⃣ Making Calls

* Select an assistant → Enter phone number
* Initiate AI-powered calls
* Monitor call duration & status

### 5️⃣ WhatsApp Conversations

* Configure **Twilio WhatsApp**
* AI assistants respond to text & voice messages

### 6️⃣ Voice Studio

* Preview AI voices
* Generate speech from text
* Adjust **stability** & **similarity**

---

## 🛠 Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Authentication:** bcrypt (secure password hashing)
* **APIs:**

  * Vapi.ai → AI voice calls
  * Twilio → WhatsApp integration
  * ElevenLabs → Voice generation
* **Storage:** JSON files (`users.json`, `call_history.json`)

---

## 🔧 API Configuration

### Vapi.ai Setup

1. Sign up at [vapi.ai](https://vapi.ai)
2. Get your **API Key**
3. Add it to `.env` or app settings

### Twilio Setup

1. Sign up at [twilio.com](https://www.twilio.com/)
2. Get your **Account SID** & **Auth Token**
3. Configure a **WhatsApp Business number**
4. Set webhook URL:

   ```bash
   http://your-server:5000/whatsapp-webhook
   ```

---

## 🎯 Key Features Explained

* **Real-time Call Handling**
  Detects caller speech, auto pause/resume, smooth interruptions

* **Voice Selection**
  Pre-made & custom voice options with real-time previews

* **Communication History**
  Logs for calls and WhatsApp messages with timestamps

* **User Management**
  Custom assistants saved per user with preferences

---

## 📁 Project Structure

```text
ai-voice-assistant/
├── app.py                # Main application
├── users.json            # User database
├── call_history.json     # Call history
├── call_Summary.json     # Call summaries
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

---

## 🙏 Acknowledgments

* [Vapi.ai](https://vapi.ai) – AI voice API
* [Twilio](https://www.twilio.com/) – WhatsApp integration
* [Streamlit](https://streamlit.io/) – Web framework
* [ElevenLabs](https://elevenlabs.io/) – Voice generation

---
