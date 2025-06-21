from fastapi import FastAPI, Request
from src.legal_analyzer.legal_analyzer import LegalAnalyzer
from src.defense_generator.defense_generator import DefenseGenerator

app = FastAPI()
analyzer = LegalAnalyzer()
defense_gen = DefenseGenerator()

@app.post("/api/analyze-case")
async def analyze_case(request: Request):
    data = await request.json()
    case_facts = data.get("case_facts", "")
    jurisdiction = data.get("jurisdiction", "Unknown")
    case_type = data.get("case_type", "Unknown")
    result = analyzer.analyze_case(case_facts, jurisdiction, case_type)
    return result

@app.post("/api/generate-defense")
async def generate_defense(request: Request):
    data = await request.json()
    case_facts = data.get("case_facts", "")
    similar_cases = data.get("similar_cases", [])
    jurisdiction = data.get("jurisdiction", "Unknown")
    result = defense_gen.generate_defense(case_facts, similar_cases, jurisdiction)
    return result