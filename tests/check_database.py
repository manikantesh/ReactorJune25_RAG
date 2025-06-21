#!/usr/bin/env python3
"""
Database Status Check Script

Quick script to check the current status of the legal case database.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.legal_analyzer.legal_analyzer import LegalAnalyzer

def check_database():
    """Check the current database status."""
    print("🔍 Checking Legal Case Database Status...")
    print("=" * 50)
    
    try:
        # Initialize analyzer
        analyzer = LegalAnalyzer()
        
        # Get database statistics
        stats = analyzer.get_database_stats()
        
        print(f"📊 Total Cases in Database: {stats.get('total_cases', 0)}")
        print(f"🗂️ Database Path: {stats.get('database_path', 'Unknown')}")
        
        if stats.get('total_cases', 0) == 0:
            print("\n❌ No cases found in database!")
            print("💡 Run the population script to add sample data:")
            print("   python src/utils/populate_database.py")
            return False
        
        print(f"\n🏛️ Cases by Jurisdiction:")
        jurisdictions = stats.get('jurisdictions', {})
        for jurisdiction, count in jurisdictions.items():
            print(f"   {jurisdiction}: {count} cases")
        
        print(f"\n📋 Cases by Type:")
        case_types = stats.get('case_types', {})
        for case_type, count in case_types.items():
            print(f"   {case_type}: {count} cases")
        
        # Test a simple query
        print(f"\n🔍 Testing Similar Case Search...")
        test_facts = "Contract breach case involving failure to pay for services"
        similar_cases = analyzer.find_similar_cases(test_facts, limit=3)
        
        print(f"📊 Found {len(similar_cases)} similar cases for test query")
        
        if similar_cases:
            print(f"\n📋 Sample Similar Cases:")
            for i, case in enumerate(similar_cases[:3], 1):
                print(f"   {i}. {case.case_name} ({case.court})")
                print(f"      Type: {case.case_type}, Jurisdiction: {case.jurisdiction}")
                print(f"      Holding: {case.holding[:100]}...")
                print()
        
        print("✅ Database is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

if __name__ == "__main__":
    check_database() 