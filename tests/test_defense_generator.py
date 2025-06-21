from src.defense_generator.defense_generator import DefenseGenerator

def test_generate_defense():
    generator = DefenseGenerator()
    case_facts = "State failed to pay for services under contract. Plaintiff seeks damages."
    similar_cases = [
        {"case_name": "John Doe v. State of California", "holding": "State's failure to pay was a material breach."}
    ]
    result = generator.generate_defense(case_facts, similar_cases, jurisdiction="california")
    assert 'strategy' in result
    print("Defense strategy generated successfully.") 