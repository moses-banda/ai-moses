"""
Voice Agent Module
Handles AI response generation using OpenAI
"""

from openai import OpenAI
import os


class VoiceAgent:
    """Generate voice responses using OpenAI GPT"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please set it in config/.env file"
            )
        
        self.client = OpenAI(api_key=api_key)
    
    def generate_response(self, caller_name="Friend", caller_relationship="unknown", 
                         caller_tone="neutral", status="Busy"):
        """
        Generate AI response based on caller info
        
        Args:
            caller_name: Name of caller
            caller_relationship: Relationship to caller (friend, family, etc)
            caller_tone: Tone to use (casual, formal, etc)
            status: Your current status
            
        Returns:
            str: AI generated response
        """
        prompt = f"""
You are an AI assistant for {caller_name}'s voicemail system.
Caller: {caller_name}
Relationship: {caller_relationship}
Tone to use: {caller_tone}
Your status: {status}

Generate a brief, natural voice response message (2-3 sentences max).
The message should acknowledge the call and explain your status.
Make it sound like you're speaking naturally.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly voicemail assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Hi {caller_name}, I'm currently {status.lower()}. Please leave a message."