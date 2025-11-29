"""
Voice Agent Module
Handles AI response generation using OpenAI
"""

from openai import OpenAI
"""
Voice Agent Module
Handles AI response generation using OpenAI
"""

from openai import OpenAI
import os


class VoiceAgent:
    """Generate voice responses using OpenAI GPT"""
    
    def __init__(self):
        """Initialize OpenAI and ElevenLabs clients"""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.voice_id = os.getenv('ELEVENLABS_VOICE_ID')
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in .env")
            
        self.client = OpenAI(api_key=self.openai_api_key)
        
        # Initialize ElevenLabs if key is present
        if self.elevenlabs_api_key:
            from elevenlabs.client import ElevenLabs
            self.elevenlabs = ElevenLabs(api_key=self.elevenlabs_api_key)
        else:
            self.elevenlabs = None
            print("Warning: ELEVENLABS_API_KEY not found. Voice cloning will be disabled.")

    def generate_response(self, caller_name="Friend", caller_relationship="unknown", 
                         caller_tone="neutral", status="Busy", conversation_history=None):
        """Generate AI response based on caller info and history"""
        
        system_prompt = f"""
You are Moses's personal AI voice assistant. You sound EXACTLY like him.
Your goal is to handle the call efficiently but warmly, using his mannerisms.
Current Status: {status}

Caller Info:
- Name: {caller_name}
- Relationship: {caller_relationship}
- Tone: {caller_tone}

Instructions:
1. Be concise. This is a voice conversation.
2. If the caller asks to leave a message, acknowledge it.
3. If the caller asks something you can't answer, say you'll pass it on to Moses.
4. Use natural fillers like "uh", "yeah", "got it" sparingly to sound human.
"""
        messages = [{"role": "system", "content": system_prompt}]
        
        if conversation_history:
            messages.extend(conversation_history)
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o", # Faster model
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating text response: {e}")
            return "I'm sorry, I'm having trouble hearing you. Please leave a message."

    def text_to_speech(self, text, output_path):
        """Convert text to speech using ElevenLabs"""
        if not self.elevenlabs or not self.voice_id:
            return False
            
        try:
            from elevenlabs import save
            audio = self.elevenlabs.generate(
                text=text,
                voice=self.voice_id,
                model="eleven_turbo_v2" # Low latency model
            )
            
            # Save audio to file
            save(audio, output_path)
            return True
        except Exception as e:
            print(f"Error generating audio: {e}")
            return False

    def generate_summary(self, conversation_text):
        """Generate a summary of the call for Moses"""
        prompt = f"""
Summarize this call for Moses as if you are his personal secretary giving a quick voice note.
Focus on: Who called, what they wanted, and any action items.
Keep it under 30 seconds spoken.

Call Transcript:
{conversation_text}
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Could not generate summary."