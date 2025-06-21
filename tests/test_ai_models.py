#!/usr/bin/env python3
"""
AI Models Test Script for Legal AI Assistant

Tests and demonstrates Claude AI models for legal analysis tasks.
"""

import sys
import os
sys.path.append('.')

from src.ai_models.model_manager import AIModelManager
from src.ai_models.claude_client import ClaudeClient

def test_model_manager():
    """Test the AI model manager."""
    print("🤖 Testing AI Model Manager")
    print("=" * 50)
    
    try:
        # Initialize model manager
        manager = AIModelManager()
        
        # Get model information
        info = manager.get_model_info()
        
        print(f"📊 Available Models: {info['available_models']}")
        print(f"🔧 Model Selection: {info['model_selection']}")
        print(f"⚙️ Performance Settings: {info['performance_settings']}")
        print(f"🔑 API Keys Configured: {info['api_keys_configured']}")
        
        if not info['available_models']:
            print("❌ No AI models available. Please check your Anthropic API key.")
            return False
        
        # Test each available model
        for model_name in info['available_models']:
            print(f"\n🧪 Testing {model_name}...")
            if manager.test_model(model_name):
                print(f"✅ {model_name} is working correctly")
            else:
                print(f"❌ {model_name} test failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing model manager: {e}")
        return False

def test_claude_client():
    """Test Claude AI model client."""
    print("\n🔍 Testing Claude Client")
    print("=" * 50)
    
    if os.getenv("ANTHROPIC_API_KEY"):
        print("\n🤖 Testing Claude Client...")
        try:
            claude = ClaudeClient()
            
            # Test case analysis
            case_facts = "Defendant charged with theft of $1,500 from retail store"
            result = claude.analyze_case(case_facts, "california", "criminal")
            print(f"✅ Claude case analysis: {len(result['analysis'])} characters")
            
            # Test defense generation
            similar_cases = [{"case_name": "State v. Johnson", "holding": "Defendant guilty of petty theft"}]
            result = claude.generate_defense_strategy(case_facts, similar_cases, "california")
            print(f"✅ Claude defense generation: {len(result['strategy'])} characters")
            
            # Test precedent analysis
            case_text = "This case involves a contract dispute between two software companies..."
            result = claude.analyze_precedent("Sample Case", case_text)
            print(f"✅ Claude precedent analysis: {len(result['analysis'])} characters")
            
            return True
            
        except Exception as e:
            print(f"❌ Claude test failed: {e}")
            return False
    else:
        print("⚠️ Anthropic API key not found - skipping Claude tests")
        return False

def test_legal_analysis():
    """Test comprehensive legal analysis with Claude."""
    print("\n⚖️ Testing Legal Analysis")
    print("=" * 50)
    
    try:
        manager = AIModelManager()
        
        # Test case analysis
        case_facts = """
        Client is a software developer who entered into a contract with TechCorp to develop 
        a custom application. The contract specified a delivery date of March 1, 2023, and 
        payment of $50,000 upon completion. Client completed the work on time, but TechCorp 
        refused to pay, claiming the software had bugs and didn't meet specifications.
        """
        
        print("📋 Testing Case Analysis...")
        result = manager.analyze_case(case_facts, "california", "civil")
        print(f"✅ Analysis completed using {result['model_used']}")
        print(f"📝 Analysis length: {len(result['analysis'])} characters")
        print(f"📄 Analysis preview: {result['analysis'][:200]}...")
        
        # Test defense strategy generation
        print("\n🛡️ Testing Defense Strategy Generation...")
        similar_cases = [
            {
                "case_name": "Wilson v. Construction Co.",
                "holding": "Judgment for plaintiff, contractor breached contract"
            },
            {
                "case_name": "Smith v. ABC Corporation", 
                "holding": "Summary judgment granted for defendant"
            }
        ]
        
        result = manager.generate_defense_strategy(case_facts, similar_cases, "california")
        print(f"✅ Strategy generated using {result['model_used']}")
        print(f"📝 Strategy length: {len(result['strategy'])} characters")
        print(f"📄 Strategy preview: {result['strategy'][:200]}...")
        
        # Test document summarization
        print("\n📄 Testing Document Summarization...")
        doc_text = """
        IN THE SUPREME COURT OF CALIFORNIA
        Case No. S123456
        
        JOHN DOE, Plaintiff,
        v.
        STATE OF CALIFORNIA, Defendant.
        
        This case presents the issue of whether the defendant, State of California, 
        is liable for damages resulting from the alleged breach of contract with 
        the plaintiff, John Doe. The evidence presented at trial established that 
        the plaintiff entered into a valid contract with the State, and that the 
        State failed to perform its obligations under the agreement.
        """
        
        result = manager.summarize_document(doc_text)
        print(f"✅ Summary generated using {result['model_used']}")
        print(f"📝 Summary length: {len(result['summary'])} characters")
        print(f"📄 Summary preview: {result['summary'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Legal analysis test failed: {e}")
        return False

def test_model_switching():
    """Test switching between different Claude models for the same task."""
    print("\n🔄 Testing Model Switching")
    print("=" * 50)
    
    try:
        manager = AIModelManager()
        available_models = manager.get_available_models()
        
        if len(available_models) < 2:
            print("⚠️ Only one model available - model switching not applicable")
            return True
        
        case_facts = "Employee alleges wrongful termination based on age discrimination"
        
        # Test with first model
        model1 = available_models[0]
        manager.switch_model('case_analysis', model1)
        result1 = manager.analyze_case(case_facts, "california", "employment")
        print(f"✅ {model1} analysis: {len(result1['analysis'])} characters")
        
        # Test with second model (if available)
        if len(available_models) > 1:
            model2 = available_models[1]
            manager.switch_model('case_analysis', model2)
            result2 = manager.analyze_case(case_facts, "california", "employment")
            print(f"✅ {model2} analysis: {len(result2['analysis'])} characters")
            print(f"🔄 Successfully switched from {model1} to {model2}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model switching test failed: {e}")
        return False

def main():
    """Run all AI model tests."""
    print("🚀 Claude AI Models Comprehensive Test")
    print("=" * 60)
    
    results = {
        "model_manager": False,
        "claude_client": False,
        "legal_analysis": False,
        "model_switching": False
    }
    
    # Test model manager
    results["model_manager"] = test_model_manager()
    
    # Test Claude client
    results["claude_client"] = test_claude_client()
    
    # Test legal analysis
    results["legal_analysis"] = test_legal_analysis()
    
    # Test model switching
    results["model_switching"] = test_model_switching()
    
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
        print("🎉 All Claude AI model tests passed! Your AI setup is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the detailed results above.")
    
    # Show usage examples
    print("\n💡 Usage Examples:")
    print("""
# Basic usage
from src.ai_models.model_manager import AIModelManager

manager = AIModelManager()

# Analyze a case
result = manager.analyze_case(
    case_facts="Your case facts here",
    jurisdiction="california", 
    case_type="civil"
)

# Generate defense strategy
strategy = manager.generate_defense_strategy(
    case_facts="Your case facts",
    similar_cases=[{"case_name": "Example", "holding": "Example holding"}],
    jurisdiction="california"
)

# Summarize a document
summary = manager.summarize_document("Your legal document text here")

# Get model information
info = manager.get_model_info()
print(f"Available models: {info['available_models']}")
    """)

if __name__ == "__main__":
    main() 