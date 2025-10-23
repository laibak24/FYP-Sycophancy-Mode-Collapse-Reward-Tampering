"""
API Client for Commercial LLM Models
"""
import os
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai

class ModelClient:
    def __init__(self):
        """Initialize API clients for different models"""
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        print("✓ Model clients initialized")
        
    def query_gpt4(self, prompt, temperature=0.7, max_tokens=500):
        """Query GPT-4o"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error querying GPT-4: {e}")
            return None
    
    def query_claude(self, prompt, temperature=0.7, max_tokens=500):
        """Query Claude Sonnet"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error querying Claude: {e}")
            return None
    
    def query_gemini(self, prompt, temperature=0.7, max_tokens=500):
        """Query Gemini 1.5 Pro"""
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
            return response.text
        except Exception as e:
            print(f"Error querying Gemini: {e}")
            return None
