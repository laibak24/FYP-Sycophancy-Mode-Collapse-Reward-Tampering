"""
Gemini API Diagnostic Tool
Tests connection and identifies issues
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("="*70)
print("GEMINI API DIAGNOSTIC TOOL")
print("="*70)

# Step 1: Check API key
print("\n[1/4] Checking API Key...")
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("❌ GOOGLE_API_KEY not found in .env file")
    print("\nTo fix:")
    print("1. Get a key from: https://makersuite.google.com/app/apikey")
    print("2. Add to .env file: GOOGLE_API_KEY=your_key_here")
    exit(1)
elif api_key == 'your_google_key_here':
    print("❌ GOOGLE_API_KEY is placeholder value")
    print("\nTo fix:")
    print("1. Get a key from: https://makersuite.google.com/app/apikey")
    print("2. Replace placeholder in .env file with actual key")
    exit(1)
else:
    print(f"✓ API key found: {api_key[:10]}...{api_key[-4:]}")

# Step 2: Import and test
print("\n[2/4] Testing Gemini SDK...")
try:
    import google.generativeai as genai
    print("✓ google-generativeai package installed")
except ImportError:
    print("❌ google-generativeai not installed")
    print("\nTo fix: pip install google-generativeai")
    exit(1)

# Step 3: Configure
print("\n[3/4] Configuring Gemini client...")
try:
    genai.configure(api_key=api_key)
    print("✓ Client configured")
except Exception as e:
    print(f"❌ Configuration failed: {e}")
    exit(1)

# Step 4: Test simple query
print("\n[4/4] Testing simple query...")

test_prompts = [
    "What is 2+2?",
    "What is 15 × 7?",
    "What is the square root of 144?"
]

for i, prompt in enumerate(test_prompts, 1):
    print(f"\n  Test {i}: {prompt}")
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.3,
                'max_output_tokens': 50,
            }
        )
        
        # Check response
        if hasattr(response, 'text') and response.text:
            print(f"  ✓ Response: {response.text.strip()[:50]}")
        else:
            print(f"  ⚠️  No text in response")
            print(f"  Candidates: {response.candidates}")
            if response.candidates:
                print(f"  Finish reason: {response.candidates[0].finish_reason}")
                print(f"  Safety ratings: {response.candidates[0].safety_ratings}")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        if "quota" in str(e).lower():
            print("\n  Quota Error Detected:")
            print("  • Free tier: 2 requests/minute, 1500 requests/day")
            print("  • Wait 1 minute between tests")
            print("  • Check usage: https://ai.dev/usage")
        elif "invalid" in str(e).lower():
            print("\n  Invalid API Key:")
            print("  • Verify key at: https://makersuite.google.com/app/apikey")
            print("  • Make sure billing is enabled (if required)")

print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70)

print("\nCommon Issues & Solutions:")
print("\n1. Rate Limit (429 errors):")
print("   • Free tier: 2 req/min, 1500 req/day")
print("   • Solution: Add delays between requests")
print("   • Upgrade: https://ai.google.dev/pricing")

print("\n2. Safety Filters (finish_reason: 2):")
print("   • Gemini blocks certain prompts")
print("   • Solution: Rephrase questions more neutrally")
print("   • Example: 'What is X?' instead of 'Calculate X'")

print("\n3. Invalid API Key:")
print("   • Get key: https://makersuite.google.com/app/apikey")
print("   • Enable Gemini API in Google Cloud Console")

print("\n4. Model Not Available:")
print("   • Try: gemini-1.5-flash (faster, cheaper)")
print("   • Try: gemini-pro (older, more stable)")

print("\n" + "="*70)