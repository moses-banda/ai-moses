"""
Twilio Handler Module
Handles incoming calls and SMS from Twilio
"""

# MUST load env variables FIRST
from dotenv import load_dotenv
import os

# Load .env from config directory
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env')
load_dotenv(dotenv_path)

from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse


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
    
    # If we have audio, play it; otherwise speak the text
    if audio_url:
        response.play(audio_url)
    else:
        # Fallback to text-to-speech with a more natural male voice
        response.say(ai_response, voice='Polly.Matthew', language='en-US')
    
    # End the call after the response
    response.hangup()
    
    return str(response), 200, {'Content-Type': 'application/xml'}


def handle_incoming_sms(ai_response_text):
    """
    Generate TwiML response for SMS
    """
    response = MessagingResponse()
    response.message(ai_response_text)
    
    return str(response), 200, {'Content-Type': 'application/xml'}