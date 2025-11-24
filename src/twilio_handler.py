from twilio.twiml.voice_response import VoiceResponse
from src.database import Database
from src.voice_agent import VoiceAgent
from src.caller_profiler import get_caller_profile
from src.status_manager import get_current_status
import json

db = Database()
voice_agent = VoiceAgent()

def handle_incoming_call(request):
    """When someone calls your number"""
    caller_phone = request.form.get('From')
    
    # Get caller info from DB
    caller_profile = get_caller_profile(caller_phone)
    
    # Get your current status
    current_status = get_current_status()
    
    # Generate personalized response
    response_text = voice_agent.generate_response(
        caller_name=caller_profile.get('name'),
        caller_history=caller_profile.get('usual_topics'),
        current_status=current_status.get('activity')
    )
    
    # Create Twilio response (text-to-speech)
    response = VoiceResponse()
    response.say(response_text, voice='alice')  # Or your custom voice
    
    # Log the call
    log_call(caller_phone, caller_profile.get('name'), response_text)
    
    return str(response)

def log_call(phone, name, transcript):
    """Record call in logs"""
    with open('logs/call_logs.json', 'a') as f:
        json.dump({
            'phone': phone,
            'name': name,
            'transcript': transcript,
            'timestamp': str(datetime.now())
        }, f)
        f.write('\n')