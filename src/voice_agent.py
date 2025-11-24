import os
from openai import OpenAI

class VoiceAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4-turbo"
    
    def generate_response(self, caller_name, caller_history, current_status):
        """Generate personalized response based on caller + your status"""
        prompt = f"""
        You are answering as {os.getenv('YOUR_NAME')}.
        Caller: {caller_name}
        Your current activity: {current_status}
        Previous conversation topics: {caller_history}
        
        Keep it natural, brief, and sound like yourself.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content