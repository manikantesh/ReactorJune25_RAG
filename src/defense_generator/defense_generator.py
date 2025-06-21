"""
Defense Generator for AI Legal Assistant

Generates comprehensive legal defense strategies using Claude models and precedent analysis.
"""

from typing import Dict, List, Any
from src.ai_models.claude_client import ClaudeClient

class DefenseGenerator:
    """Generates legal defense strategies using Claude and precedent analysis."""
    
    def __init__(self, claude_client: ClaudeClient = None):
        self.claude_client = claude_client or ClaudeClient()
    
    def generate_defense(self, case_facts: str, similar_cases: List[Dict], jurisdiction: str = "Unknown") -> Dict[str, Any]:
        """Generate a defense strategy for a new case.
        
        Args:
            case_facts: Facts of the new case
            similar_cases: List of similar cases (dicts or objects)
            jurisdiction: Legal jurisdiction
            
        Returns:
            Dictionary containing the generated defense strategy
        """
        return self.claude_client.generate_defense_strategy(case_facts, similar_cases, jurisdiction) 