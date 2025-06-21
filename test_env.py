#!/usr/bin/env python3
"""
Test script to check environment variable loading
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"✅ OpenAI API key found: {api_key[:20]}...")
else:
    print("❌ OpenAI API key not found")

# Check other important variables
database_url = os.getenv('DATABASE_URL')
if database_url:
    print(f"✅ Database URL found: {database_url}")
else:
    print("❌ Database URL not found")

print("\nAll environment variables:")
for key, value in os.environ.items():
    if 'KEY' in key or 'URL' in key:
        if value and not value.startswith('your_'):
            print(f"{key}: {value[:50]}...")
        else:
            print(f"{key}: {value}") 