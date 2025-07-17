# System Architecture Overview

## High-Level Architecture

The Abstract Screening Tool follows a pipeline architecture that transforms research protocol screening criteria into automated abstract screening decisions.

## Core Components

### 1. User Interface Layer
- **Streamlit GUI**: Web-based interface for researchers
- **Input Handlers**: Comprehensive screening criteria input (PIC + additional exclusions) and CSV file upload
- **Input Format**: Expected columns Reference ID, Title, Abstract text
- **Results Display**: Reference ID, Title, Decision, Reasoning based on all screening criteria

### 2. Data Processing Layer
- **Criteria Parser**: Extracts and structures inclusion/exclusion criteria from protocols
- **Abstract Processor**: Handles CSV imports from academic databases
- **Prompt Generator**: Converts all screening criteria into LLM-optimized prompts

### 3. LLM Integration Layer
- **API Clients**: OpenAI and Anthropic API interfaces
- **Prompt Engineering**: Structured prompts for consistent criteria-based screening
- **Response Parser**: Converts LLM outputs to structured binary decisions

### 4. Output Layer
- **Decision Formatter**: Structures include/exclude decisions
- **CSV Exporter**: Generates results in importable format
- **Audit Trail**: Maintains criteria-based reasoning transparency

## Data Flow

```
Research Protocol (Word/PDF)
    ↓
[User copies all screening criteria]
    ↓
Streamlit GUI Input Form
    ↓
Criteria Parser & Validator
    ↓
Abstract CSV Upload
    ↓
Abstract Processor & Cleaner
    ↓
Prompt Generator
    ↓
LLM API Call (OpenAI/Anthropic)
    ↓
Response Parser & Validator
    ↓
Decision Formatter
    ↓
CSV Export with Results
```

## Key Design Decisions

### Comprehensive Criteria Approach
- Supports established PIC methodology (Population, Intervention, Comparator)
- Handles additional exclusion criteria (geographic, design, language restrictions)
- Ensures clinical and methodological relevance of screening criteria
- Provides structured framework for LLM prompts
- All reasoning must explicitly reference violated criteria

### Streamlit for GUI
- Familiar to research community
- Rapid prototyping and deployment
- Built-in file upload and data display capabilities

### LLM API Integration
- Model flexibility (can switch between providers)
- No local model hosting requirements
- Leverages latest language model capabilities

### CSV-Based Workflow
- Compatible with standard academic databases
- Easy integration with existing review management tools
- Transparent, auditable data pipeline

## Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **NLP Processing**: NLTK, spaCy, transformers
- **Data Handling**: pandas, numpy
- **LLM APIs**: OpenAI API, Anthropic API
- **File Processing**: openpyxl, python-docx

## Security Considerations

- API key management via environment variables
- No persistent storage of sensitive research data
- Session-based file handling in Streamlit

## Scalability Notes

- Designed for typical systematic review volumes (1,000-10,000 abstracts)
- Batch processing for LLM API efficiency
- Configurable rate limiting for API compliance