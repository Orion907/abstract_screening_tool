# Functional Requirements

## Core Functionality

### FR-001: Screening Criteria Input
**Description**: System shall accept screening criteria via unified text input

**Requirements**:
- Single text area for Population, Intervention, Comparison (PIC)  criteria or custom prompts
- Support copy/paste from research protocols or existing prompts
- Provide PIC template for users creating criteria from scratch
- Handle formatting inconsistencies in pasted text
- Validate that input area contains screening criteria

### FR-002: Abstract File Upload
**Description**: System shall accept research abstracts in CSV format

**Requirements**:
- Support CSV file upload (up to 10MB)
- Validate required columns: Reference ID, Title, Abstract text
- Handle common academic database export formats
- Display upload status and file summary

### FR-003: Automated Abstract Screening
**Description**: System shall screen abstracts using LLM API

**Requirements**:
- Generate structured prompts from user screening criteria
- Process abstracts in configurable batches with progress tracking
- Handle API rate limits and errors gracefully
- Support multiple LLM providers (OpenAI, Anthropic)

### FR-004: Screening Results Output
**Description**: System shall provide structured screening decisions

**Requirements**:
- Return Include/Exclude/Uncertain decision for each abstract
- Provide reasoning text for each decision
- Maintain original abstract metadata (title, authors, DOI, etc.)
- Generate downloadable CSV with results and audit trail

## User Interface Requirements

### UI-001: Streamlit Interface
**Description**: Single-page web application with clear workflow

**Requirements**:
- Unified text area for screening criteria input
- CSV file upload with validation
- Progress tracking during processing
- Results display and download
- Real-time error messages and guidance

## Technical Requirements

### API-001: LLM Integration
**Description**: Support multiple LLM providers with robust error handling

**Requirements**:
- OpenAI and Anthropic API integration
- Configurable model selection
- Retry failed requests with exponential backoff
- Rate limiting compliance and meaningful error messages

### DP-001: Data Processing
**Description**: Prepare text for effective LLM processing

**Requirements**:
- Clean HTML tags and normalize formatting from abstracts
- Generate structured prompts from user screening criteria
- Handle text encoding issues (UTF-8)
- Truncate overly long abstracts if necessary

## Quality Assurance

### QA-001: Reliability and Transparency
**Description**: Ensure consistent, auditable screening process

**Requirements**:
- Use standardized prompt templates for consistency
- Maintain complete audit trail (inputs, outputs, timestamps)
- Log API interactions for troubleshooting
- Support manual review of uncertain decisions
- Enable reconstruction of all screening decisions