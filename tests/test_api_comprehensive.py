#!/usr/bin/env python3
"""
Comprehensive API Test Script for Legal AI Assistant

Tests all API endpoints with various scenarios to ensure proper functionality.
"""

import requests
import json
import time
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

def test_database_stats():
    """Test the database statistics endpoint."""
    print("\n🔍 Testing Database Statistics...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/database-stats")
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get('database_stats', {})
            
            print(f"✅ Database stats retrieved successfully")
            print(f"📊 Total cases: {stats.get('total_cases', 0)}")
            print(f"🏛️ Jurisdictions: {stats.get('jurisdictions', {})}")
            print(f"📋 Case types: {stats.get('case_types', {})}")
            
            return stats.get('total_cases', 0) > 0
        else:
            print(f"❌ Failed to get database stats: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing database stats: {e}")
        return False

def test_case_analysis(case_facts: str, jurisdiction: str = "california", case_type: str = "civil"):
    """Test the case analysis endpoint."""
    print(f"\n🔍 Testing Case Analysis...")
    print(f"📝 Case facts: {case_facts[:100]}...")
    
    try:
        payload = {
            "case_facts": case_facts,
            "jurisdiction": jurisdiction,
            "case_type": case_type
        }
        
        response = requests.post(f"{BASE_URL}/api/analyze-case", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            analysis = data.get('analysis', {})
            
            print(f"✅ Case analysis completed successfully")
            print(f"📊 Similar cases found: {len(analysis.get('similar_cases', []))}")
            print(f"⚖️ Precedents found: {len(analysis.get('precedents', []))}")
            print(f"🎯 Confidence score: {analysis.get('confidence_score', 0):.2f}")
            
            return True
        else:
            print(f"❌ Failed to analyze case: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing case analysis: {e}")
        return False

def test_defense_generation(case_facts: str, jurisdiction: str = "california", case_type: str = "civil"):
    """Test the defense generation endpoint."""
    print(f"\n🔍 Testing Defense Generation...")
    print(f"📝 Case facts: {case_facts[:100]}...")
    
    try:
        payload = {
            "case_facts": case_facts,
            "jurisdiction": jurisdiction,
            "case_type": case_type
        }
        
        response = requests.post(f"{BASE_URL}/api/generate-defense", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            defense = data.get('defense_strategy', {})
            
            print(f"✅ Defense strategy generated successfully")
            print(f"📋 Arguments generated: {len(defense.get('arguments', []))}")
            print(f"📚 Citations provided: {len(defense.get('citations', []))}")
            print(f"🎯 Confidence score: {defense.get('confidence_score', 0):.2f}")
            
            return True
        else:
            print(f"❌ Failed to generate defense: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing defense generation: {e}")
        return False

def test_document_parsing(file_path: str):
    """Test the document parsing endpoint."""
    print(f"\n🔍 Testing Document Parsing...")
    print(f"📄 File: {file_path}")
    
    try:
        payload = {
            "file_path": file_path
        }
        
        response = requests.post(f"{BASE_URL}/api/parse-document", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            parsed_doc = data.get('parsed_document', {})
            
            print(f"✅ Document parsed successfully")
            print(f"📋 File type: {parsed_doc.get('file_type', 'unknown')}")
            print(f"🏛️ Court: {parsed_doc.get('extracted_info', {}).get('court', 'unknown')}")
            print(f"📅 Date: {parsed_doc.get('extracted_info', {}).get('date', 'unknown')}")
            
            return True
        else:
            print(f"❌ Failed to parse document: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing document parsing: {e}")
        return False

def run_comprehensive_tests():
    """Run all comprehensive tests."""
    print("🚀 Starting Comprehensive API Tests...")
    
    # Test cases for different scenarios
    test_cases = [
        {
            "name": "Contract Breach Case",
            "facts": "Client entered into a contract with a construction company for kitchen renovation. The contractor failed to complete the work on time and the quality was substandard. Client seeks damages for breach of contract.",
            "jurisdiction": "california",
            "case_type": "civil"
        },
        {
            "name": "Criminal Theft Case",
            "facts": "Defendant charged with theft of $1,500 from retail store. Security camera footage shows defendant taking items without paying. Defendant claims items were purchased but receipt was lost.",
            "jurisdiction": "california",
            "case_type": "criminal"
        },
        {
            "name": "Employment Discrimination Case",
            "facts": "Employee alleges wrongful termination based on age discrimination. Employee was 58 years old when terminated and replaced by employee 25 years younger. Employee had good performance record.",
            "jurisdiction": "federal",
            "case_type": "employment"
        },
        {
            "name": "Personal Injury Case",
            "facts": "Plaintiff injured in slip and fall on city sidewalk. Sidewalk had known defect for 6 months. City had received multiple complaints about the dangerous condition.",
            "jurisdiction": "california",
            "case_type": "civil"
        },
        {
            "name": "Family Law Case",
            "facts": "Divorce proceeding with minor children. Dispute over child custody and support. Both parents have stable employment and suitable living arrangements.",
            "jurisdiction": "california",
            "case_type": "family"
        }
    ]
    
    # Test document parsing
    sample_documents = [
        "data/sample_documents/sample_judgment.txt",
        "data/sample_documents/sample_brief.txt",
        "data/sample_documents/sample_criminal_case.txt",
        "data/sample_documents/sample_employment_case.txt",
        "data/sample_documents/sample_family_case.txt"
    ]
    
    results = {
        "database_stats": False,
        "case_analysis": [],
        "defense_generation": [],
        "document_parsing": []
    }
    
    # Test database stats
    results["database_stats"] = test_database_stats()
    
    # Test case analysis for each scenario
    for i, test_case in enumerate(test_cases):
        print(f"\n{'='*60}")
        print(f"📋 Test Case {i+1}: {test_case['name']}")
        print(f"{'='*60}")
        
        # Test case analysis
        analysis_success = test_case_analysis(
            test_case["facts"],
            test_case["jurisdiction"],
            test_case["case_type"]
        )
        results["case_analysis"].append({
            "name": test_case["name"],
            "success": analysis_success
        })
        
        # Test defense generation
        defense_success = test_defense_generation(
            test_case["facts"],
            test_case["jurisdiction"],
            test_case["case_type"]
        )
        results["defense_generation"].append({
            "name": test_case["name"],
            "success": defense_success
        })
        
        # Add delay between requests
        time.sleep(1)
    
    # Test document parsing
    print(f"\n{'='*60}")
    print("📄 Testing Document Parsing")
    print(f"{'='*60}")
    
    for doc_path in sample_documents:
        parsing_success = test_document_parsing(doc_path)
        results["document_parsing"].append({
            "file": doc_path,
            "success": parsing_success
        })
        time.sleep(0.5)
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    print(f"✅ Database Stats: {'PASS' if results['database_stats'] else 'FAIL'}")
    
    analysis_success_count = sum(1 for r in results["case_analysis"] if r["success"])
    print(f"✅ Case Analysis: {analysis_success_count}/{len(results['case_analysis'])} PASS")
    
    defense_success_count = sum(1 for r in results["defense_generation"] if r["success"])
    print(f"✅ Defense Generation: {defense_success_count}/{len(results['defense_generation'])} PASS")
    
    parsing_success_count = sum(1 for r in results["document_parsing"] if r["success"])
    print(f"✅ Document Parsing: {parsing_success_count}/{len(results['document_parsing'])} PASS")
    
    # Print detailed results
    print(f"\n📋 Detailed Results:")
    
    print(f"\n🔍 Case Analysis Results:")
    for result in results["case_analysis"]:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"  {status} - {result['name']}")
    
    print(f"\n🛡️ Defense Generation Results:")
    for result in results["defense_generation"]:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"  {status} - {result['name']}")
    
    print(f"\n📄 Document Parsing Results:")
    for result in results["document_parsing"]:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"  {status} - {result['file']}")
    
    # Overall success rate
    total_tests = 1 + len(results["case_analysis"]) + len(results["defense_generation"]) + len(results["document_parsing"])
    successful_tests = (1 if results["database_stats"] else 0) + analysis_success_count + defense_success_count + parsing_success_count
    
    print(f"\n🎯 Overall Success Rate: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the detailed results above.")
    
    return results

if __name__ == "__main__":
    run_comprehensive_tests() 