from src.legal_analyzer.legal_analyzer import LegalAnalyzer

def test_find_similar_cases():
    analyzer = LegalAnalyzer()
    case_facts = "State failed to pay for services under contract. Plaintiff seeks damages."
    similar_cases = analyzer.find_similar_cases(case_facts, jurisdiction="california", case_type="civil", limit=2)
    assert isinstance(similar_cases, list)
    print(f"Found {len(similar_cases)} similar cases.") 