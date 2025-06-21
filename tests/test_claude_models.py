#!/usr/bin/env python3
"""
Test script to check available Claude models
"""

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

def test_claude_models():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ No Anthropic API key found")
        return
    
    print(f"✅ Found API key: {api_key[:20]}...")
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Test with a simple message to see what models work
        test_models = [
            "claude-3-sonnet-20240229",
            "claude-3-sonnet",
            "claude-3-haiku-20240307",
            "claude-3-haiku",
            "claude-3-opus-20240229",
            "claude-3-opus"
        ]
        
        for model in test_models:
            try:
                print(f"\nTesting model: {model}")
                message = client.messages.create(
                    model=model,
                    max_tokens=10,
                    messages=[{"role": "user", "content": "Hello"}]
                )
                print(f"✅ {model} works!")
                break
            except Exception as e:
                print(f"❌ {model} failed: {str(e)[:100]}...")
                
    except Exception as e:
        print(f"❌ Error connecting to Anthropic API: {e}")

if __name__ == "__main__":
    test_claude_models() 