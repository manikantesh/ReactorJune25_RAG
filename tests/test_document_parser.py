import os
from src.document_processor.document_parser import DocumentParser

def test_parse_sample_judgment():
    parser = DocumentParser()
    file_path = 'data/sample_documents/sample_judgment.txt'
    result = parser.parse_document(file_path)
    assert result['file_type'] == 'txt'
    assert 'case_name' in result['extracted_info']
    assert 'court' in result['extracted_info']
    assert 'holding' in result['extracted_info']
    print("Sample judgment parsed successfully.")

def test_parse_sample_brief():
    parser = DocumentParser()
    file_path = 'data/sample_documents/sample_brief.txt'
    result = parser.parse_document(file_path)
    assert result['file_type'] == 'txt'
    assert 'case_name' in result['extracted_info']
    print("Sample brief parsed successfully.") 