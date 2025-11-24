from flask import Flask, request
from src.twilio_handler import handle_incoming_call
from src.voice_agent import VoiceAgent
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
voice_agent = VoiceAgent()

@app.route('/incoming-call', methods=['POST'])
def incoming_call():
    """Twilio sends call here"""
    return handle_incoming_call(request)

@app.route('/update-status', methods=['POST'])
def update_status():
    """Update your current activity"""
    from src.status_manager import update_status
    data = request.json
    return update_status(data.get('activity'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)