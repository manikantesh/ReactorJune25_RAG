"""
Legal Analyzer for AI Legal Assistant

Handles legal case analysis, precedent matching, and legal research
using AI models and vector databases.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import numpy as np
from datetime import datetime

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from ..ai_models.openai_client import OpenAIClient

logger = logging.getLogger(__name__)


@dataclass
class Case:
    """Data class for legal case information."""
    case_name: str
    court: str
    date: str
    jurisdiction: str
    case_type: str
    key_facts: List[str]
    legal_issues: List[str]
    holding: str
    reasoning: List[str]
    citation: Optional[str] = None
    judges: Optional[List[str]] = None
    parties: Optional[List[str]] = None
    embedding: Optional[List[float]] = None


@dataclass
class AnalysisResult:
    """Data class for legal analysis results."""
    case_analysis: Dict[str, Any]
    similar_cases: List[Case]
    precedents: List[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    confidence_score: float


class LegalAnalyzer:
    """Main legal analyzer for case analysis and precedent matching."""
    
    def __init__(self, 
                 vector_db_path: Optional[str] = None,
                 openai_client: Optional[OpenAIClient] = None,
                 config: Optional[Dict] = None):
        """Initialize the legal analyzer.
        
        Args:
            vector_db_path: Path to vector database
            openai_client: OpenAI client instance
            config: Configuration dictionary
        """
        self.config = config or {}
        self.vector_db_path = vector_db_path or "./data/chroma_db"
        self.openai_client = openai_client or OpenAIClient()
        
        # Initialize vector database
        self._init_vector_db()
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load legal rules
        self.legal_rules = self._load_legal_rules()
        
    def _init_vector_db(self):
        """Initialize the vector database."""
        try:
            self.chroma_client = chromadb.PersistentClient(
                path=self.vector_db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="legal_cases",
                metadata={"description": "Legal cases and precedents"}
            )
            
            logger.info(f"Vector database initialized at {self.vector_db_path}")
            
        except Exception as e:
            logger.error(f"Error initializing vector database: {e}")
            raise
    
    def _load_legal_rules(self) -> Dict[str, Any]:
        """Load legal rules and frameworks."""
        rules_path = self.config.get('legal_rules_path', 'config/legal_rules.yaml')
        
        if os.path.exists(rules_path):
            import yaml
            with open(rules_path, 'r') as file:
                return yaml.safe_load(file)
        else:
            # Default rules
            return {
                'jurisdictions': {
                    'federal': {'name': 'Federal Courts'},
                    'california': {'name': 'California Courts'},
                    'new_york': {'name': 'New York Courts'}
                },
                'case_types': {
                    'criminal': ['felony', 'misdemeanor', 'infraction'],
                    'civil': ['contract', 'tort', 'property', 'family', 'employment']
                }
            }
    
    def add_case_to_database(self, case: Case) -> bool:
        """Add a case to the vector database.
        
        Args:
            case: Case object to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate embedding for the case
            case_text = self._prepare_case_text(case)
            embedding = self.embedding_model.encode(case_text).tolist()
            
            # Prepare metadata
            metadata = {
                'case_name': case.case_name,
                'court': case.court,
                'date': case.date,
                'jurisdiction': case.jurisdiction,
                'case_type': case.case_type,
                'citation': case.citation or '',
                'judges': json.dumps(case.judges or []),
                'parties': json.dumps(case.parties or [])
            }
            
            # Add to collection
            self.collection.add(
                embeddings=[embedding],
                documents=[case_text],
                metadatas=[metadata],
                ids=[f"case_{len(self.collection.get()['ids'])}"]
            )
            
            logger.info(f"Added case to database: {case.case_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding case to database: {e}")
            return False
    
    def find_similar_cases(self, 
                          case_facts: str, 
                          jurisdiction: Optional[str] = None,
                          case_type: Optional[str] = None,
                          limit: int = 10) -> List[Case]:
        """Find similar cases based on case facts.
        
        Args:
            case_facts: Facts of the current case
            jurisdiction: Target jurisdiction
            case_type: Type of case
            limit: Maximum number of similar cases to return
            
        Returns:
            List of similar cases
        """
        try:
            # Generate embedding for case facts
            embedding = self.embedding_model.encode(case_facts).tolist()
            
            # Prepare query
            query_embeddings = [embedding]
            n_results = limit
            
            # Add filters if specified
            where_clause = {}
            if jurisdiction:
                where_clause['jurisdiction'] = jurisdiction
            if case_type:
                where_clause['case_type'] = case_type
            
            # Query the database
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results,
                where=where_clause if where_clause else None
            )
            
            # Convert results to Case objects
            similar_cases = []
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0], 
                results['metadatas'][0], 
                results['distances'][0]
            )):
                case = Case(
                    case_name=metadata.get('case_name', 'Unknown'),
                    court=metadata.get('court', 'Unknown'),
                    date=metadata.get('date', 'Unknown'),
                    jurisdiction=metadata.get('jurisdiction', 'Unknown'),
                    case_type=metadata.get('case_type', 'Unknown'),
                    key_facts=self._extract_facts_from_text(doc),
                    legal_issues=self._extract_issues_from_text(doc),
                    holding=self._extract_holding_from_text(doc),
                    reasoning=self._extract_reasoning_from_text(doc),
                    citation=metadata.get('citation'),
                    judges=json.loads(metadata.get('judges', '[]')),
                    parties=json.loads(metadata.get('parties', '[]')),
                    embedding=results['embeddings'][0][i] if results['embeddings'] else None
                )
                similar_cases.append(case)
            
            logger.info(f"Found {len(similar_cases)} similar cases")
            return similar_cases
            
        except Exception as e:
            logger.error(f"Error finding similar cases: {e}")
            return []
    
    def analyze_case(self, 
                    case_facts: str, 
                    jurisdiction: str, 
                    case_type: str) -> AnalysisResult:
        """Perform comprehensive case analysis.
        
        Args:
            case_facts: Facts of the case
            jurisdiction: Legal jurisdiction
            case_type: Type of case
            
        Returns:
            Analysis result object
        """
        try:
            # Find similar cases
            similar_cases = self.find_similar_cases(
                case_facts, jurisdiction, case_type, limit=5
            )
            
            # Analyze case using AI
            case_analysis = self.openai_client.analyze_case(
                case_facts, jurisdiction, case_type
            )
            
            # Analyze precedents
            precedents = []
            for case in similar_cases[:3]:  # Analyze top 3 similar cases
                precedent_analysis = self.openai_client.analyze_precedent(
                    case.case_name, 
                    self._prepare_case_text(case)
                )
                precedents.append({
                    'case': case,
                    'analysis': precedent_analysis
                })
            
            # Perform risk assessment
            risk_assessment = self._assess_risk(case_facts, similar_cases, jurisdiction)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                case_analysis, similar_cases, risk_assessment
            )
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(
                case_analysis, precedents, len(similar_cases)
            )
            
            return AnalysisResult(
                case_analysis=case_analysis,
                similar_cases=similar_cases,
                precedents=precedents,
                risk_assessment=risk_assessment,
                recommendations=recommendations,
                confidence_score=confidence_score
            )
            
        except Exception as e:
            logger.error(f"Error in case analysis: {e}")
            raise
    
    def _prepare_case_text(self, case: Case) -> str:
        """Prepare case text for embedding and analysis."""
        text_parts = [
            f"Case: {case.case_name}",
            f"Court: {case.court}",
            f"Date: {case.date}",
            f"Jurisdiction: {case.jurisdiction}",
            f"Case Type: {case.case_type}"
        ]
        
        if case.key_facts:
            text_parts.append("Key Facts: " + " ".join(case.key_facts))
        
        if case.legal_issues:
            text_parts.append("Legal Issues: " + " ".join(case.legal_issues))
        
        if case.holding:
            text_parts.append(f"Holding: {case.holding}")
        
        if case.reasoning:
            text_parts.append("Reasoning: " + " ".join(case.reasoning))
        
        return " | ".join(text_parts)
    
    def _extract_facts_from_text(self, text: str) -> List[str]:
        """Extract key facts from text."""
        # Simplified extraction - in practice, this would be more sophisticated
        sentences = text.split('.')
        fact_keywords = ['alleged', 'evidence', 'witness', 'testimony', 'found']
        
        facts = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in fact_keywords):
                if len(sentence.strip()) > 20:
                    facts.append(sentence.strip())
        
        return facts[:5]  # Return top 5 facts
    
    def _extract_issues_from_text(self, text: str) -> List[str]:
        """Extract legal issues from text."""
        sentences = text.split('.')
        issue_keywords = ['issue', 'question', 'whether', 'claim']
        
        issues = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in issue_keywords):
                if len(sentence.strip()) > 20:
                    issues.append(sentence.strip())
        
        return issues[:3]  # Return top 3 issues
    
    def _extract_holding_from_text(self, text: str) -> str:
        """Extract holding from text."""
        holding_keywords = ['hold', 'holding', 'conclude', 'find', 'determine']
        
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in holding_keywords):
                if len(sentence.strip()) > 30:
                    return sentence.strip()
        
        return "Holding not found"
    
    def _extract_reasoning_from_text(self, text: str) -> List[str]:
        """Extract reasoning from text."""
        sentences = text.split('.')
        reasoning_keywords = ['because', 'therefore', 'thus', 'consequently']
        
        reasoning = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in reasoning_keywords):
                if len(sentence.strip()) > 30:
                    reasoning.append(sentence.strip())
        
        return reasoning[:3]  # Return top 3 reasoning statements
    
    def _assess_risk(self, 
                    case_facts: str, 
                    similar_cases: List[Case], 
                    jurisdiction: str) -> Dict[str, Any]:
        """Assess risk level for the case."""
        # Count favorable vs unfavorable outcomes
        favorable_count = 0
        unfavorable_count = 0
        
        for case in similar_cases:
            holding_lower = case.holding.lower()
            if any(word in holding_lower for word in ['grant', 'favor', 'win', 'success']):
                favorable_count += 1
            elif any(word in holding_lower for word in ['deny', 'dismiss', 'lose', 'fail']):
                unfavorable_count += 1
        
        total_cases = len(similar_cases)
        if total_cases == 0:
            risk_level = "unknown"
            risk_score = 0.5
        else:
            favorable_ratio = favorable_count / total_cases
            
            if favorable_ratio >= 0.7:
                risk_level = "low"
                risk_score = 0.2
            elif favorable_ratio >= 0.4:
                risk_level = "medium"
                risk_score = 0.5
            else:
                risk_level = "high"
                risk_score = 0.8
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'favorable_cases': favorable_count,
            'unfavorable_cases': unfavorable_count,
            'total_similar_cases': total_cases,
            'favorable_ratio': favorable_count / total_cases if total_cases > 0 else 0
        }
    
    def _generate_recommendations(self, 
                                case_analysis: Dict[str, Any],
                                similar_cases: List[Case],
                                risk_assessment: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Add recommendations based on risk level
        if risk_assessment['risk_level'] == 'high':
            recommendations.append("Consider settlement negotiations early in the process")
            recommendations.append("Focus on strong evidence collection and witness preparation")
        elif risk_assessment['risk_level'] == 'medium':
            recommendations.append("Prepare comprehensive defense strategy")
            recommendations.append("Consider expert witness testimony")
        else:
            recommendations.append("Proceed with confidence but maintain thorough preparation")
        
        # Add recommendations based on similar cases
        if similar_cases:
            recommendations.append(f"Study {len(similar_cases)} similar cases for precedent")
        
        # Add general recommendations
        recommendations.extend([
            "Ensure all evidence is properly documented and preserved",
            "Prepare witnesses thoroughly for testimony",
            "Consider alternative dispute resolution if appropriate"
        ])
        
        return recommendations
    
    def _calculate_confidence(self, 
                            case_analysis: Dict[str, Any],
                            precedents: List[Dict[str, Any]],
                            similar_cases_count: int) -> float:
        """Calculate confidence score for the analysis."""
        # Base confidence from AI analysis
        base_confidence = case_analysis.get('confidence', 0.5)
        
        # Adjust based on number of similar cases
        case_factor = min(similar_cases_count / 5.0, 1.0)  # Normalize to 0-1
        
        # Adjust based on precedent analysis quality
        precedent_confidence = 0.5
        if precedents:
            precedent_confidences = [p['analysis'].get('confidence', 0.5) for p in precedents]
            precedent_confidence = sum(precedent_confidences) / len(precedent_confidences)
        
        # Weighted average
        confidence = (base_confidence * 0.4 + case_factor * 0.3 + precedent_confidence * 0.3)
        
        return min(confidence, 1.0)  # Cap at 1.0
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the case database."""
        try:
            collection_data = self.collection.get()
            total_cases = len(collection_data['ids'])
            
            # Count by jurisdiction
            jurisdictions = {}
            for metadata in collection_data['metadatas']:
                jurisdiction = metadata.get('jurisdiction', 'Unknown')
                jurisdictions[jurisdiction] = jurisdictions.get(jurisdiction, 0) + 1
            
            # Count by case type
            case_types = {}
            for metadata in collection_data['metadatas']:
                case_type = metadata.get('case_type', 'Unknown')
                case_types[case_type] = case_types.get(case_type, 0) + 1
            
            return {
                'total_cases': total_cases,
                'jurisdictions': jurisdictions,
                'case_types': case_types,
                'database_path': self.vector_db_path
            }
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {'error': str(e)} 