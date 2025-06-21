"""
AI Model Manager for Legal AI Assistant

Unified interface for managing Claude AI models for legal document analysis,
case analysis, and defense strategy generation.
"""

import os
import yaml
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

from .claude_client import ClaudeClient

logger = logging.getLogger(__name__)

class AIModelManager:
    """Manages Claude AI models for legal analysis tasks."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the AI model manager.
        
        Args:
            config_path: Path to AI models configuration file
        """
        self.config_path = config_path or "config/ai_models.yaml"
        self.config = self._load_config()
        
        # Initialize available models
        self.models = {}
        self._initialize_models()
        
        # Set default model selection
        self.model_selection = self.config.get('model_selection', {})
        
    def _load_config(self) -> Dict[str, Any]:
        """Load AI models configuration."""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error loading AI config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration if config file is not available."""
        return {
            'model_selection': {
                'case_analysis': 'claude-3-haiku-20240307',
                'defense_generation': 'claude-3-haiku-20240307',
                'precedent_analysis': 'claude-3-haiku-20240307',
                'document_summarization': 'claude-3-haiku-20240307'
            },
            'performance': {
                'batch_size': 10,
                'max_concurrent_requests': 5,
                'timeout_seconds': 30,
                'retry_attempts': 3
            }
        }
    
    def _initialize_models(self):
        """Initialize available Claude models."""
        try:
            # Initialize Claude if API key is available
            if os.getenv("ANTHROPIC_API_KEY"):
                self.models['claude-3-haiku-20240307'] = ClaudeClient()
                logger.info("✅ Claude model initialized")
            else:
                logger.warning("⚠️ Anthropic API key not found - Claude model not available")
                
        except Exception as e:
            logger.error(f"Error initializing models: {e}")
    
    def get_model(self, task_type: str) -> Any:
        """Get the appropriate model for a given task type.
        
        Args:
            task_type: Type of task (case_analysis, defense_generation, etc.)
            
        Returns:
            Claude client instance
        """
        # Get preferred model for task
        preferred_model = self.model_selection.get(task_type, 'claude-3-haiku-20240307')
        
        # Check if preferred model is available
        if preferred_model in self.models:
            return self.models[preferred_model]
        
        # Fallback to available models
        available_models = list(self.models.keys())
        if available_models:
            fallback_model = available_models[0]
            logger.warning(f"Preferred model {preferred_model} not available, using {fallback_model}")
            return self.models[fallback_model]
        
        raise ValueError("No AI models available. Please check your Anthropic API key.")
    
    def analyze_case(self, case_facts: str, jurisdiction: str, case_type: str) -> Dict[str, Any]:
        """Analyze a legal case using Claude."""
        model = self.get_model('case_analysis')
        return model.analyze_case(case_facts, jurisdiction, case_type)
    
    def generate_defense_strategy(self, case_facts: str, similar_cases: List[Dict], jurisdiction: str) -> Dict[str, Any]:
        """Generate defense strategy using Claude."""
        model = self.get_model('defense_generation')
        return model.generate_defense_strategy(case_facts, similar_cases, jurisdiction)
    
    def analyze_precedent(self, case_name: str, case_text: str) -> Dict[str, Any]:
        """Analyze legal precedent using Claude."""
        model = self.get_model('precedent_analysis')
        return model.analyze_precedent(case_name, case_text)
    
    def summarize_document(self, document_text: str) -> Dict[str, Any]:
        """Summarize legal document using Claude."""
        model = self.get_model('document_summarization')
        return self._claude_summarize(model, document_text)
    
    def _claude_summarize(self, model: Any, document_text: str) -> Dict[str, Any]:
        """Summarize document using Claude."""
        prompt = f"""
Please provide a comprehensive summary of this legal document:

{document_text[:3000]}

Focus on:
1. Key facts and issues
2. Legal principles involved
3. Court's decision
4. Important reasoning
5. Practical implications
"""
        summary = model._call_claude(prompt, "You are a legal document analyst.")
        return {"summary": summary, "model_used": getattr(model, 'model_name', 'claude-3-haiku-20240307')}
    
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        return list(self.models.keys())
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about available models and configuration."""
        return {
            'available_models': self.get_available_models(),
            'model_selection': self.model_selection,
            'performance_settings': self.config.get('performance', {}),
            'api_keys_configured': {
                'anthropic': bool(os.getenv("ANTHROPIC_API_KEY"))
            }
        }
    
    def switch_model(self, task_type: str, model_name: str):
        """Switch the model used for a specific task type.
        
        Args:
            task_type: Type of task
            model_name: Name of the model to use
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} is not available")
        
        self.model_selection[task_type] = model_name
        logger.info(f"Switched {task_type} to use {model_name}")
    
    def test_model(self, model_name: str) -> bool:
        """Test if a model is working correctly.
        
        Args:
            model_name: Name of the model to test
            
        Returns:
            True if model is working, False otherwise
        """
        if model_name not in self.models:
            return False
        
        try:
            model = self.models[model_name]
            # Simple test prompt
            test_prompt = "Please respond with 'OK' if you can see this message."
            response = model._call_claude(test_prompt)
            return 'OK' in response or len(response) > 0
            
        except Exception as e:
            logger.error(f"Model test failed for {model_name}: {e}")
            return False 