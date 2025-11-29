"""
Twilio Handler Module
Handles incoming calls from Twilio
"""

# MUST load env variables FIRST
from dotenv import load_dotenv
import os

# Load .env from config directory
"""
Twilio Handler Module
Handles incoming calls from Twilio
"""

# MUST load env variables FIRST
from dotenv import load_dotenv
import os

# Load .env from config directory
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env')
load_dotenv(dotenv_path)

from twilio.twiml.voice_response import VoiceResponse


def handle_incoming_call(request, ai_response=None, audio_url=None):
    """
    Handle incoming Twilio call
    
    Args:
        request: Flask request object
        ai_response: AI generated response text
        audio_url: URL to generated audio file (optional)
        
    Returns:
        TwiML response for Twilio
    """
    if ai_response is None:
        ai_response = "Hello, I'm currently unavailable. Please leave a message."
    
    response = VoiceResponse()
    
    if audio_url:
        response.play(audio_url)
    else:
        response.say(ai_response, voice='alice')
        
    # Configure status callback to trigger summary generation
    response.record(
        max_length=60, 
        action='/incoming-call', 
        method='POST',
        recording_status_callback='/call-status',
        recording_status_callback_event='completed'
    )
    
    return str(response)