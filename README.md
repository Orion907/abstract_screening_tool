# Abstract Screening Tool

A Streamlit-based tool for automating systematic review abstract screening using Large Language Models (LLMs) and PICOTS criteria.

## Overview

This tool streamlines the initial abstract screening phase of systematic reviews by:
- Accepting PICOTS criteria (Population, Intervention, Comparison, Outcome, Timeframe, Study design) from research protocols
- Processing uploaded research abstracts in CSV format
- Using natural language processing to create LLM-comprehensible prompts
- Automatically screening abstracts via LLM API calls
- Returning structured screening decisions with reasoning

## Key Features

- **PICOTS Integration**: Copy/paste criteria from Word document protocols
- **Streamlit GUI**: User-friendly interface for researchers
- **Multiple LLM Support**: Compatible with OpenAI and Anthropic APIs
- **Structured Output**: Returns title, author, include/exclude decision, and reasoning
- **CSV Workflow**: Handles common academic database export formats

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run src/main.py
```

## Project Structure

```
abstract_screening_tool/
├── src/                    # Application source code
├── tests/                  # Unit and integration tests
├── docs/                   # Project documentation
├── data/                   # Sample data and user uploads
├── config/                 # Configuration files
└── requirements.txt        # Python dependencies
```

## Documentation

- **[System Architecture](docs/architecture/system-overview.md)** - Technical overview and data flow
- **[Requirements](docs/requirements/functional-requirements.md)** - Detailed feature specifications
- **[Development Setup](docs/development/setup.md)** - Environment configuration and testing
- **[User Guide](docs/user/user-guide.md)** - How to use the tool

## Target Users

Research teams conducting systematic reviews who need to screen large volumes of abstracts efficiently while maintaining transparency and auditability in their inclusion/exclusion decisions.

## License

[To be determined]

## Contributing

See [Development Guide](docs/development/setup.md) for setup instructions and contribution guidelines.