#!/usr/bin/env python3
"""
Environment Test Script for Legal AI Assistant

Tests the environment setup and configuration for the legal AI assistant.
"""

import os
import sys
from pathlib import Path

def test_environment():
    """Test the environment setup."""
    print("🔍 Testing Environment Setup")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    else:
        print("✅ Python version is compatible")
    
    # Check working directory
    cwd = os.getcwd()
    print(f"📁 Working directory: {cwd}")
    
    # Check if we're in the project root
    if Path("src").exists() and Path("config").exists():
        print("✅ Project structure looks correct")
    else:
        print("❌ Not in project root directory")
        return False
    
    return True

def test_api_keys():
    """Test API key configuration."""
    print("\n🔑 Testing API Keys")
    print("=" * 50)
    
    # Check Anthropic API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        print(f"✅ Anthropic API key found: {api_key[:20]}...")
    else:
        print("❌ Anthropic API key not found")
    
    return bool(api_key)

def test_dependencies():
    """Test if required dependencies are available."""
    print("\n📦 Testing Dependencies")
    print("=" * 50)
    
    required_packages = [
        'anthropic',
        'chromadb', 
        'sentence_transformers',
        'yaml',
        'fastapi',
        'uvicorn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_data_directories():
    """Test if required data directories exist."""
    print("\n📂 Testing Data Directories")
    print("=" * 50)
    
    required_dirs = [
        'data',
        'data/chroma_db',
        'data/court_records',
        'data/processed_data',
        'data/sample_documents'
    ]
    
    missing_dirs = []
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path}")
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"\n⚠️ Missing directories: {', '.join(missing_dirs)}")
        print("These will be created automatically when needed")
    
    return True

def test_config_files():
    """Test if configuration files exist."""
    print("\n⚙️ Testing Configuration Files")
    print("=" * 50)
    
    config_files = [
        'config/ai_models.yaml',
        'config/legal_rules.yaml'
    ]
    
    missing_files = []
    
    for file_path in config_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Missing config files: {', '.join(missing_files)}")
        return False
    
    return True

def main():
    """Run all environment tests."""
    print("🚀 Environment Test for Legal AI Assistant")
    print("=" * 60)
    
    results = {
        "environment": False,
        "api_keys": False,
        "dependencies": False,
        "data_directories": False,
        "config_files": False
    }
    
    # Run tests
    results["environment"] = test_environment()
    results["api_keys"] = test_api_keys()
    results["dependencies"] = test_dependencies()
    results["data_directories"] = test_data_directories()
    results["config_files"] = test_config_files()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 Environment is properly configured!")
    else:
        print("⚠️ Some environment issues found. Check the results above.")
    
    # Show setup instructions
    print("\n💡 Setup Instructions:")
    print("""
1. Install dependencies:
   pip install -r requirements.txt

2. Set environment variables:
   export ANTHROPIC_API_KEY="your_anthropic_api_key_here"

3. Run the AI models test:
   python test_ai_models.py

4. Start the API server:
   python api/main.py
    """)

if __name__ == "__main__":
    main() 