"""
Database Population Script for Legal AI Assistant

Populates the ChromaDB vector database with sample legal documents and test cases.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.legal_analyzer.legal_analyzer import LegalAnalyzer, Case
from src.document_processor.document_parser import DocumentParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabasePopulator:
    """Populates the legal case database with sample data."""
    
    def __init__(self, vector_db_path: str = "./data/chroma_db"):
        """Initialize the database populator.
        
        Args:
            vector_db_path: Path to the ChromaDB database
        """
        self.vector_db_path = vector_db_path
        self.analyzer = LegalAnalyzer(vector_db_path=vector_db_path)
        self.parser = DocumentParser()
        
    def populate_from_sample_documents(self):
        """Populate database from existing sample documents."""
        sample_dir = Path("data/sample_documents")
        
        if not sample_dir.exists():
            logger.error(f"Sample documents directory not found: {sample_dir}")
            return False
            
        logger.info("Processing sample documents...")
        
        # Process all supported file types
        for file_path in sample_dir.glob("*.*"):
            if file_path.suffix.lower() in ['.txt', '.pdf', '.docx']:
                try:
                    logger.info(f"Processing: {file_path}")
                    parsed_doc = self.parser.parse_document(str(file_path))
                    
                    # Create Case object from parsed document
                    case = self._create_case_from_parsed_doc(parsed_doc, file_path.name)
                    
                    # Add to database
                    success = self.analyzer.add_case_to_database(case)
                    if success:
                        logger.info(f"✅ Added case: {case.case_name}")
                    else:
                        logger.error(f"❌ Failed to add case: {case.case_name}")
                        
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
                    
        return True
    
    def add_additional_test_cases(self):
        """Add additional test cases to the database."""
        logger.info("Adding additional test cases...")
        
        additional_cases = self._generate_additional_cases()
        
        for case in additional_cases:
            try:
                success = self.analyzer.add_case_to_database(case)
                if success:
                    logger.info(f"✅ Added test case: {case.case_name}")
                else:
                    logger.error(f"❌ Failed to add test case: {case.case_name}")
            except Exception as e:
                logger.error(f"Error adding test case {case.case_name}: {e}")
    
    def _create_case_from_parsed_doc(self, parsed_doc: Dict[str, Any], filename: str) -> Case:
        """Create a Case object from parsed document data."""
        extracted_info = parsed_doc.get('extracted_info', {})
        
        # Determine case type based on filename and content
        case_type = "civil"
        content_lower = parsed_doc.get('content', '').lower()
        filename_lower = filename.lower()
        
        if "criminal" in filename_lower or "theft" in content_lower or "burglary" in content_lower:
            case_type = "criminal"
        elif "family" in filename_lower or "marriage" in content_lower or "custody" in content_lower:
            case_type = "family"
        elif "employment" in filename_lower or "employee" in content_lower or "harassment" in content_lower:
            case_type = "employment"
        elif "contract" in filename_lower or "agreement" in content_lower:
            case_type = "contract"
        
        # Determine jurisdiction based on court info and content
        jurisdiction = None
        court_info = extracted_info.get('court', '') or ''
        content_lower = parsed_doc.get('content', '').lower()
        court_info_lower = court_info.lower()

        if 'federal' in court_info_lower or 'district' in court_info_lower or 'united states' in content_lower:
            jurisdiction = "federal"
        elif 'new york' in court_info_lower or 'new york' in content_lower:
            jurisdiction = "new_york"
        elif 'india' in court_info_lower or 'india' in content_lower:
            jurisdiction = "india"
        elif 'tamil nadu' in court_info_lower or 'tamil nadu' in content_lower:
            jurisdiction = "tamil_nadu"
        elif 'delhi' in court_info_lower or 'delhi' in content_lower:
            jurisdiction = "delhi"
        elif 'gujarat' in court_info_lower or 'gujarat' in content_lower:
            jurisdiction = "gujarat"
        elif 'maharashtra' in court_info_lower or 'maharashtra' in content_lower:
            jurisdiction = "maharashtra"
        elif 'orissa' in court_info_lower or 'orissa' in content_lower:
            jurisdiction = "orissa"
        elif 'sikkim' in court_info_lower or 'sikkim' in content_lower:
            jurisdiction = "sikkim"
        else:
            jurisdiction = "california"  # fallback
        
        # Extract case name with better fallback
        case_name = extracted_info.get('case_name')
        if not case_name:
            # Try to extract from content
            content = parsed_doc.get('content', '')
            lines = content.split('\n')
            for line in lines[:10]:  # Check first 10 lines
                if 'v.' in line and len(line.strip()) > 10:
                    case_name = line.strip()
                    break
            if not case_name:
                case_name = f"Case from {filename}"
        
        # Extract court with better fallback
        court = extracted_info.get('court')
        if not court:
            content = parsed_doc.get('content', '')
            if 'supreme court' in content.lower():
                court = "Supreme Court"
            elif 'court of appeal' in content.lower():
                court = "Court of Appeal"
            elif 'district court' in content.lower():
                court = "District Court"
            elif 'superior court' in content.lower():
                court = "Superior Court"
            else:
                court = "Unknown Court"
        
        return Case(
            case_name=case_name,
            court=court,
            date=extracted_info.get('date', '2023-01-01'),
            jurisdiction=jurisdiction,
            case_type=case_type,
            key_facts=extracted_info.get('key_facts', []),
            legal_issues=extracted_info.get('legal_issues', []),
            holding=extracted_info.get('holding', 'No holding available'),
            reasoning=extracted_info.get('reasoning', []),
            citation=extracted_info.get('citation'),
            judges=extracted_info.get('judges', []),
            parties=extracted_info.get('parties', [])
        )
    
    def _generate_additional_cases(self) -> List[Case]:
        """Generate additional test cases for comprehensive testing."""
        return [
            # Criminal Cases
            Case(
                case_name="State v. Johnson",
                court="Superior Court of California",
                date="2023-05-15",
                jurisdiction="california",
                case_type="criminal",
                key_facts=[
                    "Defendant charged with theft of $1,500 from retail store",
                    "Security camera footage shows defendant taking items",
                    "Defendant claims items were purchased but receipt lost"
                ],
                legal_issues=[
                    "Whether defendant had intent to permanently deprive",
                    "Whether circumstantial evidence sufficient for conviction"
                ],
                holding="Defendant guilty of petty theft, sentenced to 30 days",
                reasoning=[
                    "Security footage clearly shows theft",
                    "Defendant's explanation not credible",
                    "Value of items exceeds $950 threshold"
                ],
                citation="CR-2023-001",
                judges=["Judge Martinez"],
                parties=["State of California", "Michael Johnson"]
            ),
            
            Case(
                case_name="People v. Rodriguez",
                court="Court of Appeal of California",
                date="2023-03-20",
                jurisdiction="california",
                case_type="criminal",
                key_facts=[
                    "Defendant convicted of assault with deadly weapon",
                    "Victim suffered serious injuries requiring surgery",
                    "Defendant claims self-defense"
                ],
                legal_issues=[
                    "Whether self-defense instruction should have been given",
                    "Whether evidence sufficient to support conviction"
                ],
                holding="Conviction affirmed, self-defense not supported by evidence",
                reasoning=[
                    "No evidence defendant was in imminent danger",
                    "Defendant initiated confrontation",
                    "Injuries disproportionate to any threat"
                ],
                citation="CA-2023-045",
                judges=["Justice Thompson", "Justice Garcia"],
                parties=["People of California", "Carlos Rodriguez"]
            ),
            
            # Civil Cases
            Case(
                case_name="Smith v. ABC Corporation",
                court="Federal District Court",
                date="2023-07-10",
                jurisdiction="federal",
                case_type="civil",
                key_facts=[
                    "Plaintiff alleges wrongful termination based on age discrimination",
                    "Plaintiff was 58 years old when terminated",
                    "Replaced by employee 25 years younger"
                ],
                legal_issues=[
                    "Whether termination was based on age discrimination",
                    "Whether employer had legitimate business reason"
                ],
                holding="Summary judgment granted for defendant, no age discrimination",
                reasoning=[
                    "Plaintiff's performance had declined significantly",
                    "Company documented performance issues",
                    "Replacement had superior qualifications"
                ],
                citation="FED-2023-089",
                judges=["Judge Williams"],
                parties=["Robert Smith", "ABC Corporation"]
            ),
            
            Case(
                case_name="Garcia v. City of Los Angeles",
                court="California Court of Appeal",
                date="2023-06-25",
                jurisdiction="california",
                case_type="civil",
                key_facts=[
                    "Plaintiff injured in slip and fall on city sidewalk",
                    "Sidewalk had known defect for 6 months",
                    "City had received multiple complaints about condition"
                ],
                legal_issues=[
                    "Whether city had notice of dangerous condition",
                    "Whether city's maintenance was reasonable"
                ],
                holding="Judgment for plaintiff, city liable for $75,000",
                reasoning=[
                    "City had actual notice of defect",
                    "Reasonable time to repair had passed",
                    "Plaintiff's injuries were foreseeable"
                ],
                citation="CA-2023-112",
                judges=["Justice Lee", "Justice Brown"],
                parties=["Maria Garcia", "City of Los Angeles"]
            ),
            
            # Employment Cases
            Case(
                case_name="Thompson v. TechStart Inc.",
                court="Superior Court of California",
                date="2023-04-18",
                jurisdiction="california",
                case_type="employment",
                key_facts=[
                    "Employee alleges sexual harassment by supervisor",
                    "Multiple incidents over 8-month period",
                    "Company failed to investigate complaints"
                ],
                legal_issues=[
                    "Whether conduct constituted sexual harassment",
                    "Whether employer failed to take appropriate action"
                ],
                holding="Jury verdict for plaintiff, $150,000 in damages",
                reasoning=[
                    "Conduct was severe and pervasive",
                    "Employer had duty to investigate",
                    "Failure to act created hostile work environment"
                ],
                citation="EMP-2023-023",
                judges=["Judge Anderson"],
                parties=["Sarah Thompson", "TechStart Inc."]
            ),
            
            # Family Law Cases
            Case(
                case_name="In re Marriage of Davis",
                court="Family Court of California",
                date="2023-08-05",
                jurisdiction="california",
                case_type="family",
                key_facts=[
                    "Divorce proceeding with minor children",
                    "Dispute over child custody and support",
                    "Both parents have stable employment"
                ],
                legal_issues=[
                    "What custody arrangement serves best interests of children",
                    "Appropriate amount of child support"
                ],
                holding="Joint custody awarded, support calculated per guidelines",
                reasoning=[
                    "Both parents capable and willing",
                    "Children benefit from both parents",
                    "Income disparity requires support payments"
                ],
                citation="FAM-2023-067",
                judges=["Judge Rodriguez"],
                parties=["Jennifer Davis", "Michael Davis"]
            ),
            
            # Contract Cases
            Case(
                case_name="Wilson v. Construction Co.",
                court="Superior Court of California",
                date="2023-09-12",
                jurisdiction="california",
                case_type="civil",
                key_facts=[
                    "Homeowner contracted for kitchen renovation",
                    "Contractor failed to complete work on time",
                    "Work quality was substandard"
                ],
                legal_issues=[
                    "Whether contractor breached contract",
                    "Appropriate measure of damages"
                ],
                holding="Judgment for plaintiff, $25,000 in damages",
                reasoning=[
                    "Contractor breached time and quality terms",
                    "Plaintiff entitled to cost of completion",
                    "Delay caused additional living expenses"
                ],
                citation="CON-2023-034",
                judges=["Judge Miller"],
                parties=["David Wilson", "ABC Construction Co."]
            ),
            
            # Property Cases
            Case(
                case_name="Brown v. Green",
                court="Superior Court of California",
                date="2023-10-20",
                jurisdiction="california",
                case_type="civil",
                key_facts=[
                    "Dispute over property line between neighbors",
                    "Survey shows encroachment by 3 feet",
                    "Defendant built fence on plaintiff's property"
                ],
                legal_issues=[
                    "Whether encroachment constitutes trespass",
                    "Appropriate remedy for property dispute"
                ],
                holding="Injunction granted, defendant must remove fence",
                reasoning=[
                    "Clear evidence of encroachment",
                    "Trespass is ongoing",
                    "Injunction is appropriate remedy"
                ],
                citation="PROP-2023-078",
                judges=["Judge Taylor"],
                parties=["John Brown", "Mary Green"]
            )
        ]
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get current database statistics."""
        return self.analyzer.get_database_stats()

def main():
    """Main function to populate the database."""
    print("🚀 Starting database population...")
    
    populator = DatabasePopulator()
    
    # Populate from existing sample documents
    print("\n📄 Processing existing sample documents...")
    populator.populate_from_sample_documents()
    
    # Add additional test cases
    print("\n➕ Adding additional test cases...")
    populator.add_additional_test_cases()
    
    # Show final statistics
    print("\n📊 Final database statistics:")
    stats = populator.get_database_stats()
    print(json.dumps(stats, indent=2))
    
    print("\n✅ Database population completed!")

if __name__ == "__main__":
    main() 