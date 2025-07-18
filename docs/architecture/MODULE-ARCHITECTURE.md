# Module Architecture Document
## Abstract Screening Tool

### Overview
This document defines the modular structure of the Abstract Screening Tool, specifying the responsibility of each component and their interactions. The architecture follows a layered approach with clear separation of concerns to support maintainable, testable, and AI-assistable development.

## Project Structure

```
abstract_screening_tool/
├── src/                           # Main application source code
│   ├── main.py                   # Streamlit application entry point
│   ├── ui/                       # User Interface Layer
│   │   ├── __init__.py
│   │   ├── streamlit_app.py      # Main Streamlit UI controller
│   │   ├── components/           # Reusable UI components
│   │   │   ├── __init__.py
│   │   │   ├── criteria_input.py # PIC criteria input form
│   │   │   ├── file_upload.py    # CSV file upload component
│   │   │   ├── progress_display.py # Processing progress bar
│   │   │   └── results_display.py # Results table and download
│   │   └── validators/           # UI input validation
│   │       ├── __init__.py
│   │       ├── file_validator.py # CSV file format validation
│   │       └── criteria_validator.py # PIC criteria validation
│   ├── core/                     # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── screening_engine.py   # Main orchestration of screening process
│   │   ├── pic_processor.py      # PIC criteria parsing and structuring
│   │   ├── abstract_processor.py # CSV processing and abstract cleaning
│   │   └── batch_processor.py    # Batch processing coordination
│   ├── llm/                      # LLM Integration Layer
│   │   ├── __init__.py
│   │   ├── prompt_generator.py   # Convert PIC criteria to LLM prompts
│   │   ├── api_clients/          # LLM API client implementations
│   │   │   ├── __init__.py
│   │   │   ├── base_client.py    # Abstract base class for LLM clients
│   │   │   ├── openai_client.py  # OpenAI API implementation
│   │   │   └── anthropic_client.py # Anthropic API implementation
│   │   ├── response_parser.py    # Parse and validate LLM responses
│   │   └── retry_handler.py      # API retry logic and rate limiting
│   ├── data/                     # Data Handling Layer
│   │   ├── __init__.py
│   │   ├── models/               # Data structures and schemas
│   │   │   ├── __init__.py
│   │   │   ├── pic.py           # PIC criteria data models
│   │   │   ├── abstract.py      # Abstract data models
│   │   │   ├── screening.py     # Screening results models
│   │   │   └── batch.py         # Batch processing models
│   │   ├── processors/           # Data transformation
│   │   │   ├── __init__.py
│   │   │   ├── csv_processor.py  # CSV import/export operations
│   │   │   ├── text_cleaner.py   # Abstract text cleaning and normalization
│   │   │   └── formatter.py      # Output formatting
│   │   └── validators/           # Data validation
│   │       ├── __init__.py
│   │       ├── schema_validator.py # Data schema validation
│   │       └── content_validator.py # Content quality checks
│   ├── utils/                    # Utilities and Infrastructure
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration management
│   │   ├── logging.py           # Logging and audit trail
│   │   ├── exceptions.py        # Custom exception classes
│   │   ├── constants.py         # Application constants
│   │   └── helpers.py           # General utility functions
│   └── services/                # External Service Integrations
│       ├── __init__.py
│       ├── api_service.py       # Generic API service base
│       └── export_service.py    # Result export services
├── tests/                        # Test Suite
│   ├── unit/                    # Unit tests by module
│   ├── integration/             # Integration tests
│   ├── fixtures/                # Test data and fixtures
│   └── conftest.py             # Pytest configuration
├── config/                       # Configuration Files
│   ├── app_config.yaml         # Application configuration
│   ├── llm_config.yaml         # LLM provider configurations
│   └── prompts/                # Prompt templates
│       ├── base_template.txt   # Base screening prompt template
│       └── pic_template.txt    # PIC criteria-specific template
├── data/                        # Data Directory
│   ├── sample/                 # Sample input files
│   ├── uploads/                # User uploaded files (temp)
│   └── exports/                # Generated output files (temp)
└── docs/                        # Documentation
    ├── api/                    # API documentation
    ├── user/                   # User guides
    └── development/            # Development documentation
```

## Layer Descriptions

### 1. User Interface Layer (`src/ui/`)
**Purpose**: Handles all user interactions through Streamlit interface

#### `ui/streamlit_app.py`
- **Responsibility**: Main Streamlit application controller
- **Functions**: Page layout, session state management, workflow coordination
- **Dependencies**: Components from `ui/components/`, core business logic
- **Notes**: This is the primary entry point for user interactions, orchestrating the entire screening workflow

#### `ui/components/` (UI Components)
- **`criteria_input.py`**: PIC criteria input form with template options
- **`file_upload.py`**: CSV file upload with drag-and-drop and validation
- **`progress_display.py`**: Real-time progress tracking during batch processing
- **`results_display.py`**: Interactive results table with filtering and download options

#### `ui/validators/` (UI Validation)
- **`file_validator.py`**: Validates uploaded CSV files for required columns and format
- **`criteria_validator.py`**: Validates PIC criteria completeness and format

### 2. Core Business Logic Layer (`src/core/`)
**Purpose**: Implements the main business logic without UI or external service dependencies

#### `core/screening_engine.py`
- **Responsibility**: Main orchestrator that coordinates the entire screening process
- **Key Methods**:
  - `process_screening_batch()`: Main entry point for screening workflow
  - `prepare_screening_data()`: Prepares data for LLM processing
  - `execute_screening()`: Coordinates LLM calls and response processing
- **Dependencies**: All other core modules, LLM layer, data layer
- **Notes**: This is the heart of the application - it implements the screening algorithm

#### `core/pic_processor.py`
- **Responsibility**: Processes PIC criteria from user input into structured format
- **Key Functions**: Parse text input, validate criteria completeness, standardize format
- **Dependencies**: Data models for PIC criteria
- **Notes**: Handles the complex task of converting free-text research criteria into machine-processable format

#### `core/abstract_processor.py`
- **Responsibility**: Processes and cleans abstract data from CSV files
- **Key Functions**: Text cleaning, normalization, metadata extraction
- **Dependencies**: Data models for abstracts, text cleaning utilities
- **Notes**: Ensures abstracts are properly formatted for LLM processing

#### `core/batch_processor.py`
- **Responsibility**: Manages batch processing of large abstract sets
- **Key Functions**: Batch size optimization, progress tracking, error recovery
- **Dependencies**: LLM clients, retry handlers
- **Notes**: Critical for handling systematic reviews with thousands of abstracts

### 3. LLM Integration Layer (`src/llm/`)
**Purpose**: Handles all Large Language Model interactions

#### `llm/prompt_generator.py`
- **Responsibility**: Converts PIC criteria into optimized LLM prompts
- **Key Functions**: Template rendering, prompt optimization, token counting
- **Dependencies**: PIC criteria data models, prompt templates
- **Notes**: This module is critical for screening accuracy - prompt quality directly impacts results

#### `llm/api_clients/` (LLM API Clients)
- **`base_client.py`**: Abstract base class defining common LLM client interface
- **`openai_client.py`**: OpenAI API implementation (GPT models)
- **`anthropic_client.py`**: Anthropic API implementation (Claude models)
- **Notes**: Abstraction allows easy switching between LLM providers

#### `llm/response_parser.py`
- **Responsibility**: Parses and validates LLM responses into structured decisions
- **Key Functions**: JSON parsing, decision validation, reasoning extraction
- **Dependencies**: Screening result data models
- **Notes**: Handles the critical task of converting LLM text responses into binary decisions

#### `llm/retry_handler.py`
- **Responsibility**: Handles API failures, rate limiting, and retry logic
- **Key Functions**: Exponential backoff, error classification, retry policies
- **Dependencies**: API clients, logging utilities
- **Notes**: Essential for reliability when processing large batches

### 4. Data Handling Layer (`src/data/`)
**Purpose**: Manages data structures, validation, and transformations

#### `data/models/` (Data Models)
- **`pic.py`**: PIC criteria data structures and validation
- **`abstract.py`**: Abstract metadata and content models
- **`screening.py`**: Screening results and reasoning models
- **`batch.py`**: Batch processing status and results models
- **Notes**: These define the core data contracts for the entire application

#### `data/processors/` (Data Processing)
- **`csv_processor.py`**: CSV import/export with error handling
- **`text_cleaner.py`**: Text normalization and cleaning utilities
- **`formatter.py`**: Output formatting for different export formats
- **Notes**: Handles the messy reality of real-world data from academic databases

#### `data/validators/` (Data Validation)
- **`schema_validator.py`**: Validates data against defined schemas
- **`content_validator.py`**: Validates content quality and completeness
- **Notes**: Ensures data integrity throughout the processing pipeline

### 5. Utilities Layer (`src/utils/`)
**Purpose**: Provides cross-cutting concerns and infrastructure

#### Core Utility Modules
- **`config.py`**: Configuration management (API keys, model settings, etc.)
- **`logging.py`**: Structured logging and audit trail generation
- **`exceptions.py`**: Custom exception hierarchy for error handling
- **`constants.py`**: Application-wide constants and enumerations
- **`helpers.py`**: General utility functions used across modules

### 6. Services Layer (`src/services/`)
**Purpose**: External service integrations and high-level operations

#### Service Modules
- **`api_service.py`**: Generic API service base class
- **`export_service.py`**: Handles various export formats and destinations
- **Notes**: Provides abstraction for external integrations

## Key Design Principles

### 1. Separation of Concerns
Each layer has a distinct responsibility:
- **UI Layer**: User interaction only
- **Core Layer**: Business logic without external dependencies
- **LLM Layer**: Language model interactions
- **Data Layer**: Data management and validation
- **Utils Layer**: Cross-cutting infrastructure

### 2. Dependency Flow
Dependencies flow downward and inward:
```
UI → Core → LLM/Data → Utils
```
No upward dependencies ensures clean, testable architecture.

### 3. Interface-Based Design
All inter-layer communication happens through well-defined interfaces, making the system:
- **Testable**: Easy to mock dependencies
- **Flexible**: Easy to swap implementations
- **AI-Friendly**: Clear contracts for code generation

### 4. Error Handling Strategy
- **Graceful Degradation**: Partial failures don't stop entire batches
- **Comprehensive Logging**: Full audit trail for research compliance
- **User-Friendly Messages**: Clear error communication to researchers

### 5. Configuration Management
- **Environment-Based**: Different configs for dev/prod
- **API Key Security**: Secure handling of sensitive credentials
- **Model Flexibility**: Easy switching between LLM providers

## Module Interaction Examples

### Typical Screening Workflow
```
1. User inputs PIC criteria → ui/components/criteria_input.py
2. User uploads CSV → ui/components/file_upload.py
3. Streamlit app validates inputs → ui/validators/
4. Core engine processes batch → core/screening_engine.py
5. PIC processor structures criteria → core/pic_processor.py
6. Abstract processor cleans data → core/abstract_processor.py
7. Prompt generator creates LLM prompts → llm/prompt_generator.py
8. LLM client makes API calls → llm/api_clients/
9. Response parser structures results → llm/response_parser.py
10. Results displayed and exported → ui/components/results_display.py
```

This architecture provides the granular control needed for AI-assisted development while maintaining clean separation of concerns and testability.