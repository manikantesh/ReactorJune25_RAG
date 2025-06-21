"""
OpenAI Client for Legal AI Assistant

Handles interactions with OpenAI models for legal document analysis,
case analysis, and defense strategy generation.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

import openai
from openai import OpenAI
import yaml

logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Configuration for OpenAI models."""
    model_name: str
    temperature: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float


class OpenAIClient:
    """Client for interacting with OpenAI models."""
    
    def __init__(self, api_key: Optional[str] = None, config_path: Optional[str] = None):
        """Initialize the OpenAI client.
        
        Args:
            api_key: OpenAI API key (defaults to environment variable)
            config_path: Path to AI model configuration file
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
            
        self.client = OpenAI(api_key=self.api_key)
        self.config = self._load_config(config_path)
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load AI model configuration."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        else:
            # Default configuration
            return {
                'models': {
                    'openai': {
                        'gpt-4': {
                            'model_name': 'gpt-4',
                            'temperature': 0.1,
                            'max_tokens': 4000,
                            'top_p': 1.0,
                            'frequency_penalty': 0.0,
                            'presence_penalty': 0.0
                        }
                    }
                }
            }
    
    def get_model_config(self, model_name: str) -> ModelConfig:
        """Get configuration for a specific model."""
        model_config = self.config['models']['openai'].get(model_name, {})
        return ModelConfig(
            model_name=model_config.get('model_name', model_name),
            temperature=model_config.get('temperature', 0.1),
            max_tokens=model_config.get('max_tokens', 4000),
            top_p=model_config.get('top_p', 1.0),
            frequency_penalty=model_config.get('frequency_penalty', 0.0),
            presence_penalty=model_config.get('presence_penalty', 0.0)
        )
    
    def analyze_case(self, case_facts: str, jurisdiction: str, case_type: str) -> Dict[str, Any]:
        """Analyze a legal case using AI.
        
        Args:
            case_facts: Facts of the case
            jurisdiction: Legal jurisdiction
            case_type: Type of case (criminal, civil, etc.)
            
        Returns:
            Analysis results
        """
        config = self.get_model_config('gpt-4')
        
        system_prompt = self.config.get('prompts', {}).get('case_analysis', {}).get('system', 
            "You are an expert legal analyst. Analyze the case and provide structured legal analysis.")
        
        user_prompt = self.config.get('prompts', {}).get('case_analysis', {}).get('user_template', 
            "Case Facts: {case_facts}\nJurisdiction: {jurisdiction}\nCase Type: {case_type}").format(
                case_facts=case_facts,
                jurisdiction=jurisdiction,
                case_type=case_type
            )
        
        try:
            response = self.client.chat.completions.create(
                model=config.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                top_p=config.top_p,
                frequency_penalty=config.frequency_penalty,
                presence_penalty=config.presence_penalty
            )
            
            analysis = response.choices[0].message.content
            
            return {
                'analysis': analysis,
                'model_used': config.model_name,
                'tokens_used': response.usage.total_tokens,
                'confidence': self._extract_confidence(analysis)
            }
            
        except Exception as e:
            logger.error(f"Error in case analysis: {e}")
            raise
    
    def generate_defense_strategy(self, case_facts: str, similar_cases: List[Dict], jurisdiction: str) -> Dict[str, Any]:
        """Generate defense strategy using AI.
        
        Args:
            case_facts: Facts of the case
            similar_cases: List of similar cases
            jurisdiction: Legal jurisdiction
            
        Returns:
            Defense strategy
        """
        config = self.get_model_config('gpt-4')
        
        system_prompt = self.config.get('prompts', {}).get('defense_generation', {}).get('system',
            "You are a skilled defense attorney. Generate comprehensive defense strategies.")
        
        similar_cases_text = "\n".join([
            f"Case: {case.get('case_name', 'Unknown')}\nHolding: {case.get('holding', 'N/A')}\n"
            for case in similar_cases[:5]  # Limit to top 5 cases
        ])
        
        user_prompt = self.config.get('prompts', {}).get('defense_generation', {}).get('user_template',
            "Case Facts: {case_facts}\nSimilar Cases: {similar_cases}\nJurisdiction: {jurisdiction}").format(
                case_facts=case_facts,
                similar_cases=similar_cases_text,
                jurisdiction=jurisdiction
            )
        
        try:
            response = self.client.chat.completions.create(
                model=config.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                top_p=config.top_p,
                frequency_penalty=config.frequency_penalty,
                presence_penalty=config.presence_penalty
            )
            
            strategy = response.choices[0].message.content
            
            return {
                'strategy': strategy,
                'model_used': config.model_name,
                'tokens_used': response.usage.total_tokens,
                'similar_cases_used': len(similar_cases),
                'confidence': self._extract_confidence(strategy)
            }
            
        except Exception as e:
            logger.error(f"Error in defense generation: {e}")
            raise
    
    def analyze_precedent(self, case_name: str, case_text: str) -> Dict[str, Any]:
        """Analyze a legal precedent using AI.
        
        Args:
            case_name: Name of the precedent case
            case_text: Text content of the case
            
        Returns:
            Precedent analysis
        """
        config = self.get_model_config('gpt-3.5-turbo')
        
        system_prompt = self.config.get('prompts', {}).get('precedent_analysis', {}).get('system',
            "You are a legal researcher. Analyze legal precedents and extract key principles.")
        
        user_prompt = self.config.get('prompts', {}).get('precedent_analysis', {}).get('user_template',
            "Precedent Case: {case_name}\nCase Text: {case_text}").format(
                case_name=case_name,
                case_text=case_text[:3000]  # Limit text length
            )
        
        try:
            response = self.client.chat.completions.create(
                model=config.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                top_p=config.top_p,
                frequency_penalty=config.frequency_penalty,
                presence_penalty=config.presence_penalty
            )
            
            analysis = response.choices[0].message.content
            
            return {
                'analysis': analysis,
                'model_used': config.model_name,
                'tokens_used': response.usage.total_tokens,
                'case_name': case_name,
                'confidence': self._extract_confidence(analysis)
            }
            
        except Exception as e:
            logger.error(f"Error in precedent analysis: {e}")
            raise
    
    def generate_embeddings(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        """Generate embeddings for text using OpenAI.
        
        Args:
            text: Text to embed
            model: Embedding model to use
            
        Returns:
            List of embedding values
        """
        try:
            response = self.client.embeddings.create(
                model=model,
                input=text
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def _extract_confidence(self, text: str) -> float:
        """Extract confidence score from AI response.
        
        This is a simplified implementation. In practice, you might want
        to use more sophisticated methods to extract confidence scores.
        """
        # Look for confidence indicators in the text
        confidence_indicators = {
            'highly confident': 0.9,
            'very confident': 0.85,
            'confident': 0.8,
            'somewhat confident': 0.7,
            'moderately confident': 0.6,
            'uncertain': 0.4,
            'not confident': 0.2
        }
        
        text_lower = text.lower()
        for indicator, score in confidence_indicators.items():
            if indicator in text_lower:
                return score
        
        # Default confidence based on text length and structure
        if len(text) > 500 and any(keyword in text_lower for keyword in ['therefore', 'conclude', 'hold']):
            return 0.75
        elif len(text) > 200:
            return 0.6
        else:
            return 0.4
    
    def batch_process(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple tasks in batch.
        
        Args:
            tasks: List of tasks to process
            
        Returns:
            List of results
        """
        results = []
        
        for task in tasks:
            try:
                if task['type'] == 'case_analysis':
                    result = self.analyze_case(
                        task['case_facts'],
                        task['jurisdiction'],
                        task['case_type']
                    )
                elif task['type'] == 'defense_generation':
                    result = self.generate_defense_strategy(
                        task['case_facts'],
                        task['similar_cases'],
                        task['jurisdiction']
                    )
                elif task['type'] == 'precedent_analysis':
                    result = self.analyze_precedent(
                        task['case_name'],
                        task['case_text']
                    )
                else:
                    raise ValueError(f"Unknown task type: {task['type']}")
                
                results.append({
                    'task_id': task.get('id'),
                    'status': 'success',
                    'result': result
                })
                
            except Exception as e:
                logger.error(f"Error processing task {task.get('id')}: {e}")
                results.append({
                    'task_id': task.get('id'),
                    'status': 'error',
                    'error': str(e)
                })
        
        return results 