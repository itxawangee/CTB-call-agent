from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Import backend modules
from . import auth, database, vapi_integration, twilio_integration

@app.route('/')
def home():
    return jsonify({"message": "AI Voice Assistant API"})

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)