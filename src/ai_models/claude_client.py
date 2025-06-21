"""
Claude Client for Legal AI Assistant

Handles interactions with Anthropic Claude models for legal document analysis,
case analysis, and defense strategy generation.
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from dotenv import load_dotenv
import anthropic

logger = logging.getLogger(__name__)
load_dotenv()

@dataclass
class ClaudeModelConfig:
    model_name: str
    max_tokens: int
    temperature: float
    system_prompt: str = ""

class ClaudeClient:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "claude-3-haiku-20240307"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model_name = "claude-3-haiku-20240307"
        self.max_tokens = 2048
        self.temperature = 0.1

    def _call_claude(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        try:
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt or "You are a helpful legal assistant.",
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text if message.content else ""
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise

    def analyze_case(self, case_facts: str, jurisdiction: str, case_type: str) -> Dict[str, Any]:
        prompt = f"""
Case Facts: {case_facts}
Jurisdiction: {jurisdiction}
Case Type: {case_type}

Please provide a comprehensive legal analysis including:
1. Key legal issues
2. Potential defenses
3. Relevant precedents
4. Risk assessment
5. Recommended strategy
"""
        system_prompt = "You are an expert legal analyst with deep knowledge of case law and legal precedents."
        analysis = self._call_claude(prompt, system_prompt)
        return {"analysis": analysis, "model_used": self.model_name}

    def generate_defense_strategy(self, case_facts: str, similar_cases: List[Dict], jurisdiction: str) -> Dict[str, Any]:
        similar_cases_text = "\n".join([
            f"Case: {case.get('case_name', 'Unknown')}\nHolding: {case.get('holding', 'N/A')}\n"
            for case in similar_cases[:5]
        ])
        prompt = f"""
Case Facts: {case_facts}
Similar Cases: {similar_cases_text}
Jurisdiction: {jurisdiction}

Generate a defense strategy including:
1. Primary defense arguments
2. Supporting evidence requirements
3. Witness strategy
4. Cross-examination points
5. Closing argument framework
"""
        system_prompt = "You are a skilled defense attorney with expertise in crafting legal arguments."
        strategy = self._call_claude(prompt, system_prompt)
        return {"strategy": strategy, "model_used": self.model_name}

    def analyze_precedent(self, case_name: str, case_text: str) -> Dict[str, Any]:
        prompt = f"""
Precedent Case: {case_name}
Case Text: {case_text[:3000]}

Extract and analyze:
1. Key legal principles
2. Court's reasoning
3. Applicable holdings
4. Distinguishing factors
5. Relevance to similar cases
"""
        system_prompt = "You are a legal researcher specializing in case law analysis."
        analysis = self._call_claude(prompt, system_prompt)
        return {"analysis": analysis, "model_used": self.model_name} 