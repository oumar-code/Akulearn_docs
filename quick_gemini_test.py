#!/usr/bin/env python3
import os
import sys

# Set API key from .env or direct
api_key = os.getenv('GEMINI_API_KEY') or 'AIzaSyAKRhQqNZrRVorErDlfGzQuEnqIz17D2OQ'
os.environ['GEMINI_API_KEY'] = api_key

try:
    import google.generativeai as gen
    print("[1] google-generativeai imported")
    
    gen.configure(api_key=api_key)
    print("[2] Gemini configured")
    
    model = gen.GenerativeModel('gemini-2.0-flash')
    print("[3] Model loaded")
    
    resp = model.generate_content("Say 'Gemini is working' in 1 sentence")
    print(f"[4] RESPONSE: {resp.text}")
    print("\n[SUCCESS] Gemini API is fully functional!")
    sys.exit(0)
    
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
