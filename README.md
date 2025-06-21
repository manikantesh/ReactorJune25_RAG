# Legal AI Assistant

A comprehensive legal AI assistant that uses Claude AI models to analyze legal cases, generate defense strategies, and provide legal document analysis. Built with ChromaDB for vector storage and FastAPI for the web interface.

## Features

- **Case Analysis**: AI-powered legal case analysis using Claude
- **Defense Strategy Generation**: Generate comprehensive defense strategies based on case facts and precedents
- **Document Processing**: Multi-format document ingestion (PDF, DOCX, TXT)
- **Vector Search**: Semantic search through legal precedents and case law
- **API Interface**: RESTful API for integration with other systems
- **Multi-format Support**: Process legal documents in PDF, DOCX, and TXT formats

## Architecture

- **AI/ML**: Anthropic Claude
- **Vector Database**: ChromaDB
- **Web Framework**: FastAPI
- **Document Processing**: PyPDF2, python-docx
- **Embeddings**: Sentence Transformers

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
```

### 3. Test the Setup

```bash
# Test environment
python test_env.py

# Test AI models
python test_ai_models.py
```

### 4. Populate Database with Sample Data

```bash
python create_sample_documents.py
python src/utils/populate_database.py
```

### 5. Start the API Server

```bash
python api/main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Case Analysis
- `POST /analyze-case` - Analyze a legal case
- `POST /generate-defense` - Generate defense strategy
- `POST /analyze-precedent` - Analyze legal precedent

### Document Management
- `POST /ingest-document` - Ingest legal documents
- `GET /search-cases` - Search through case database
- `GET /case/{case_id}` - Get specific case details

### Health Check
- `GET /health` - API health status

## Project Structure

```
ReactorJune25_RAG/
├── api/                    # FastAPI application
├── config/                 # Configuration files
├── data/                   # Data storage
│   ├── chroma_db/         # Vector database
│   ├── court_records/     # Legal documents
│   └── sample_documents/  # Sample data
├── src/                   # Source code
│   ├── ai_models/        # AI model clients
│   ├── defense_generator/ # Defense strategy generation
│   ├── document_processor/ # Document processing
│   ├── legal_analyzer/    # Legal analysis
│   └── utils/            # Utility functions
└── tests/                # Test files
```

## Configuration

### AI Models (`config/ai_models.yaml`)
Configure Claude models and prompts for different legal analysis tasks.

### Legal Rules (`config/legal_rules.yaml`)
Define legal rules and precedents for analysis.

## Usage Examples

### Basic Case Analysis

```python
from src.ai_models.model_manager import AIModelManager

manager = AIModelManager()

# Analyze a case
result = manager.analyze_case(
    case_facts="Defendant charged with theft of $1,500",
    jurisdiction="california",
    case_type="criminal"
)

print(result['analysis'])
```

### Defense Strategy Generation

```python
# Generate defense strategy
strategy = manager.generate_defense_strategy(
    case_facts="Your case facts here",
    similar_cases=[{"case_name": "Example", "holding": "Example holding"}],
    jurisdiction="california"
)

print(strategy['strategy'])
```

### Document Summarization

```python
# Summarize legal document
summary = manager.summarize_document("Your legal document text here")
print(summary['summary'])
```

## Testing

Run comprehensive tests:

```bash
# Test environment setup
python test_env.py

# Test AI models
python test_ai_models.py

# Test API endpoints
python test_api_comprehensive.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.