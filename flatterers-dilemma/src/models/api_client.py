"""
API Client for Commercial LLM Models
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai

class ModelClient:
    def __init__(self):
        """Initialize API clients for different models"""
        
        # Get API keys from environment
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        google_key = os.getenv('GOOGLE_API_KEY')
        
        if not openai_key:
            print("⚠ Warning: OPENAI_API_KEY not found in environment")
        if not anthropic_key:
            print("⚠ Warning: ANTHROPIC_API_KEY not found in environment")
        if not google_key:
            print("⚠ Warning: GOOGLE_API_KEY not found in environment")
        
        self.openai_client = OpenAI(api_key=openai_key) if openai_key else None
        self.anthropic_client = Anthropic(api_key=anthropic_key) if anthropic_key else None
        
        if google_key:
            genai.configure(api_key=google_key)
        
        print("✓ Model clients initialized")
        
    def query_gpt4(self, prompt, temperature=0.7, max_tokens=500):
        """Query GPT-4o"""
        if not self.openai_client:
            print("✗ OpenAI client not initialized. Check your API key.")
            return None
            
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
        if not self.anthropic_client:
            print("✗ Anthropic client not initialized. Check your API key.")
            return None
            
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
        """Query Gemini (using latest available model)"""
        try:
            # Use the most capable available model
            model = genai.GenerativeModel('gemini-2.5-pro')  # ✓ This exists!
            
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