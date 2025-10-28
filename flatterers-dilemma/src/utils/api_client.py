"""
API Client for Commercial LLM Models
"""

import os
import time
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
from dotenv import load_dotenv

# ------------------------------------------------------------------
# 🔐 Load Environment Variables
# ------------------------------------------------------------------
load_dotenv()


class ModelClient:
    def __init__(self):
        """Initialize API clients for GPT-4o, Claude, and Gemini"""
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        print("✅ Model clients initialized successfully.")

    # ------------------------------------------------------------------
    # 🧠 GPT-4o Query
    # ------------------------------------------------------------------
    def query_gpt4(self, prompt, temperature=0.7, max_tokens=500):
        """Query GPT-4o"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_completion_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ GPT-4o Error: {e}")
            return None

    # ------------------------------------------------------------------
    # 🤖 Claude 3.5 Sonnet Query
    # ------------------------------------------------------------------
    def query_claude(self, prompt, temperature=0.7, max_tokens=500):
        """Query Claude 3.5 Sonnet"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            if hasattr(response, "content") and len(response.content) > 0:
                return response.content[0].text.strip()
            else:
                return "(No response text returned from Claude)"
        except Exception as e:
            print(f"❌ Claude 3.5 Error: {e}")
            return None

    # ------------------------------------------------------------------
    # 🌟 Gemini 2.5 Pro Query (with Retry & Timeout)
    # ------------------------------------------------------------------
    def query_gemini(
        self,
        prompt,
        temperature=0.7,
        max_tokens=500,
        retries=3,
        use_flash=False,
    ):
        """
        Query Gemini 2.5 (Pro or Flash)
        Automatically retries on transient failures.
        """
        # ✅ Use your verified models
        model_name = (
            "models/gemini-2.5-flash"
            if use_flash
            else "models/gemini-2.5-pro"
        )

        for attempt in range(retries):
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    ),
                )

                # ✅ Return plain text output
                if hasattr(response, "text") and response.text:
                    return response.text.strip()

                # Fallback structure
                if (
                    hasattr(response, "candidates")
                    and len(response.candidates) > 0
                    and hasattr(response.candidates[0], "content")
                    and response.candidates[0].content.parts
                ):
                    return response.candidates[0].content.parts[0].text.strip()

                return "(No response text returned from Gemini)"

            except Exception as e:
                print(f"⚠️ Gemini Error (attempt {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    print("❌ Gemini API failed after multiple retries.")
                    return None
