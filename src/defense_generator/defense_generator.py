"""
Defense Generator for AI Legal Assistant

Generates comprehensive legal defense strategies using AI models and precedent analysis.
"""

from typing import Dict, List, Any
from ..ai_models.openai_client import OpenAIClient

class DefenseGenerator:
    """Generates legal defense strategies using AI and precedent analysis."""
    
    def __init__(self, openai_client: OpenAIClient = None):
        self.openai_client = openai_client or OpenAIClient()
    
    def generate_defense(self, case_facts: str, similar_cases: List[Dict], jurisdiction: str = "Unknown") -> Dict[str, Any]:
        """Generate a defense strategy for a new case.
        
        Args:
            case_facts: Facts of the new case
            similar_cases: List of similar cases (dicts or objects)
            jurisdiction: Legal jurisdiction
            
        Returns:
            Dictionary containing the generated defense strategy
        """
        return self.openai_client.generate_defense_strategy(case_facts, similar_cases, jurisdiction) 