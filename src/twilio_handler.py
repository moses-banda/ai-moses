"""
Twilio Handler Module
Handles incoming calls from Twilio
"""

# MUST load env variables FIRST
from dotenv import load_dotenv
load_dotenv()

from twilio.twiml.voice_response import VoiceResponse
import os


def handle_incoming_call(request, ai_response=None):
    """
    Handle incoming Twilio call
    
    Args:
        request: Flask request object
        ai_response: AI generated response text
        
    Returns:
        TwiML response for Twilio
    """
    if ai_response is None:
        ai_response = "Hello, I'm currently unavailable. Please leave a message."
    
    response = VoiceResponse()
    response.say(ai_response, voice='alice')
    response.record(max_length=60, action='/incoming-call', method='POST')
    
    return str(response)