# Demo Mode Implementation Plan

## Demo Constraints & Advantages
- **Known CSV format**: Exact column structure predetermined
- **Pre-screened ground truth**: Manual screening already completed
- **Controlled conditions**: No edge cases or unknown inputs
- **Success metric**: Accuracy comparison with expert reviewers
- **Timeline**: 3-4 days to working demo

## Implementation Priority Order

### **Phase 1: Core Data Models** (Day 1 Morning)
**Essential modules only:**
1. `data/models/pic.py` - Simplified PIC criteria storage
2. `data/models/abstract.py` - Basic abstract data structure
3. `data/models/screening.py` - Simple Include/Exclude results

**Demo simplifications:**
- Basic validation only (not empty checks)
- Fixed field structure (no optional complexity)
- Minimal error handling

### **Phase 2: Data Processing** (Day 1 Afternoon)
**Focus on known format:**
1. `data/processors/csv_processor.py` - Hard-coded for demo CSV format
2. `data/processors/text_cleaner.py` - Basic cleaning only

**Demo approach:**
- Assume specific column names
- No format detection needed
- Basic text cleaning sufficient

### **Phase 3: LLM Integration** (Day 2 Morning)
**Single provider, working prompts:**
1. `llm/prompt_generator.py` - Convert PIC criteria to screening prompts
2. `llm/api_clients/openai_client.py` - One provider only (OpenAI or Anthropic)
3. `llm/response_parser.py` - Parse Include/Exclude decisions

**Demo focus:**
- One well-tested prompt template
- Basic retry logic
- Simple response parsing

### **Phase 4: Core Business Logic** (Day 2 Afternoon)
**Essential screening workflow:**
1. `core/screening_engine.py` - Main processing orchestration
2. `core/pic_processor.py` - Convert user input to structured PIC
3. `core/batch_processor.py` - Process abstracts in batches

**Demo requirements:**
- Handle demo data volume efficiently
- Basic progress tracking
- Simple error logging

### **Phase 5: Demo UI** (Day 3)
**Streamlit interface for demo:**
1. `ui/streamlit_app.py` - Main demo interface
2. `ui/components/criteria_input.py` - PIC criteria input
3. `ui/components/file_upload.py` - CSV upload
4. `ui/components/results_display.py` - Results vs ground truth comparison

**Demo features:**
- Clean, professional appearance
- Pre-populated PIC criteria option
- Results comparison with accuracy metrics
- Export capabilities

## **Modules We Skip for Demo**
**Can implement later:**
- Advanced validation (`ui/validators/`)
- Multiple LLM providers (`llm/api_clients/anthropic_client.py`)
- Complex error handling (`utils/exceptions.py`)
- Advanced configuration (`utils/config.py`)
- Comprehensive logging (`utils/logging.py`)

## **Demo-Specific Implementation Notes**

### **Known CSV Format Assumptions**
```python
# Hard-code for demo CSV structure
EXPECTED_COLUMNS = {
    'Reference ID': 'reference_id',
    'Title': 'title', 
    'Abstract': 'abstract',
    'Manual Decision': 'ground_truth'  # For comparison
}
```

### **Simplified Error Handling**
```python
# Demo approach: fail gracefully with user-friendly messages
try:
    result = process_abstract(abstract, pic_criteria)
except Exception as e:
    result = ScreeningResult(
        decision="Error",
        reasoning=f"Processing failed: {str(e)}"
    )
```

### **Demo UI Optimizations**
```python
# Pre-populate PIC criteria for smooth demo
default_pic = """
Population: Adults with Type 2 diabetes
Intervention: Metformin therapy
Comparator: Placebo or standard care
"""
```

## **Success Criteria for Demo**

### **Functional Requirements**
- [ ] Processes demo CSV file without errors
- [ ] Returns Include/Exclude decisions with reasoning
- [ ] Calculates accuracy vs. ground truth
- [ ] Completes processing in reasonable time (<10 minutes)
- [ ] Professional UI suitable for presentation

### **Demo Metrics to Calculate**
- **Overall accuracy**: % agreement with expert reviewers
- **Precision/Recall**: Include/Exclude accuracy separately  
- **Processing speed**: Abstracts per minute
- **Consistency**: Same results on repeated runs

### **Demo Story Elements**
- **Problem**: Manual screening takes days
- **Solution**: AI screening in minutes  
- **Validation**: High accuracy vs. experts
- **Value**: Speed + consistency + audit trail

## **Post-Demo Extension Path**
**After successful demo, add:**
1. Robust error handling and edge cases
2. Multiple LLM provider support
3. Advanced validation and user feedback
4. Production deployment considerations
5. Extensive testing and quality assurance

## **Claude Code Implementation Strategy**
**When working in VSCode:**
1. **Start with data models** - Foundation first
2. **Test each module** as you build it
3. **Use demo CSV** for testing throughout
4. **Focus on working code** over perfect code
5. **Measure accuracy** against ground truth early and often

This plan gives Claude Code clear priorities and constraints for rapid, demo-focused development while maintaining the modular architecture for future expansion.