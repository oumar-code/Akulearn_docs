#!/usr/bin/env python3
import os
import sys

# Add workspace to path
sys.path.insert(0, 'c:\\Users\\hp\\Documents\\Akulearn_docs')

# Load env
from dotenv import load_dotenv
load_dotenv('c:\\Users\\hp\\Documents\\Akulearn_docs\\.env')

# Check API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
    sys.exit(1)

print(f"API Key found: {api_key[:20]}...")

# Try Gemini
try:
    import google.generativeai as gen
    gen.configure(api_key=api_key)
    print("Gemini configured successfully")
    
    # Try a simple text generation first
    print("\nTesting text generation...")
    model = gen.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Say 'Gemini is working' in one sentence.")
    print(f"Response: {response.text}")
    print("\nSUCCESS: Gemini API is working!")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    sys.exit(1)
