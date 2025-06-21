"""
FastAPI main application for Legal AI Assistant
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Load environment variables
load_dotenv()

# Import our modules
from src.legal_analyzer.legal_analyzer import LegalAnalyzer
from src.defense_generator.defense_generator import DefenseGenerator
from src.document_processor.document_parser import DocumentParser

app = FastAPI(
    title="Legal AI Assistant",
    description="AI-powered legal document analysis and defense strategy generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our services
try:
    analyzer = LegalAnalyzer()
    defense_gen = DefenseGenerator()
    doc_parser = DocumentParser()
    print("✅ All services initialized successfully")
except Exception as e:
    print(f"❌ Error initializing services: {e}")
    analyzer = None
    defense_gen = None
    doc_parser = None

# Pydantic models for request/response
class CaseAnalysisRequest(BaseModel):
    case_facts: str
    jurisdiction: str = "Unknown"
    case_type: str = "Unknown"

class DefenseRequest(BaseModel):
    case_facts: str
    similar_cases: List[Dict[str, Any]]
    jurisdiction: str = "Unknown"

class DocumentParseRequest(BaseModel):
    file_path: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Legal AI Assistant API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "analyzer": analyzer is not None,
            "defense_generator": defense_gen is not None,
            "document_parser": doc_parser is not None
        }
    }

@app.post("/api/analyze-case")
async def analyze_case(request: CaseAnalysisRequest):
    """Analyze a legal case and find similar precedents"""
    try:
        if not analyzer:
            raise HTTPException(status_code=500, detail="Legal analyzer not initialized")
        
        result = analyzer.analyze_case(
            request.case_facts,
            request.jurisdiction,
            request.case_type
        )
        
        return {
            "status": "success",
            "case_analysis": result.case_analysis,
            "similar_cases": [
                {
                    "case_name": case.case_name,
                    "court": case.court,
                    "date": case.date,
                    "jurisdiction": case.jurisdiction,
                    "case_type": case.case_type,
                    "holding": case.holding,
                    "key_facts": case.key_facts[:3],  # Limit to top 3 facts
                    "legal_issues": case.legal_issues[:2]  # Limit to top 2 issues
                }
                for case in result.similar_cases
            ],
            "risk_assessment": result.risk_assessment,
            "recommendations": result.recommendations,
            "confidence_score": result.confidence_score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/generate-defense")
async def generate_defense(request: DefenseRequest):
    """Generate defense strategy for a case"""
    try:
        if not defense_gen:
            raise HTTPException(status_code=500, detail="Defense generator not initialized")
        
        result = defense_gen.generate_defense(
            request.case_facts,
            request.similar_cases,
            request.jurisdiction
        )
        
        return {
            "status": "success",
            "defense_strategy": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Defense generation failed: {str(e)}")

@app.post("/api/parse-document")
async def parse_document(request: DocumentParseRequest):
    """Parse a legal document and extract structured information"""
    try:
        if not doc_parser:
            raise HTTPException(status_code=500, detail="Document parser not initialized")
        
        result = doc_parser.parse_document(request.file_path)
        
        return {
            "status": "success",
            "parsed_document": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document parsing failed: {str(e)}")

@app.get("/api/database-stats")
async def get_database_stats():
    """Get statistics about the case database"""
    try:
        if not analyzer:
            raise HTTPException(status_code=500, detail="Legal analyzer not initialized")
        
        stats = analyzer.get_database_stats()
        
        return {
            "status": "success",
            "database_stats": stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get database stats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)