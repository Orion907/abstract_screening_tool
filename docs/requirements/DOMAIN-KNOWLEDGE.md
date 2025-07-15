# Domain Knowledge: Implementation Context

## Systematic Review Abstract Screening

### Purpose
Systematic reviews require screening thousands of research abstracts to identify relevant studies. Traditional process involves two reviewers independently applying inclusion/exclusion criteria, then resolving disagreements. This tool automates the initial screening phase.

### Target Users
Research teams conducting systematic reviews who need to process large volumes (1,000-10,000+) of abstracts efficiently while maintaining audit trails.

## PICOTS Framework

### Implementation Requirements
PICOTS provides structured inclusion/exclusion criteria that must be converted into effective LLM prompts.

**Components and Prompt Translation:**
- **Population**: Patient/subject characteristics → Filter by demographics, conditions, settings
- **Intervention**: Treatment/exposure being studied → Identify specific therapies, procedures, exposures  
- **Comparison**: Control or alternative treatment → Distinguish intervention from control groups
- **Outcome**: Measured endpoints → Recognize relevant outcome measurements
- **Timeframe**: Study duration requirements → Validate minimum follow-up periods
- **Study Design**: Research methodology → Filter by study types (RCT, cohort, etc.)

### Technical Considerations
- Users may paste PICOTS from Word docs (handle formatting issues)
- Criteria can be incomplete or ambiguous (system should handle gracefully)
- Some users prefer custom prompts over structured PICOTS

## Abstract Screening Workflow

### Input Processing
**CSV Structure Expected:**
- Required: Title, Authors, Abstract text
- Optional: DOI, Journal, Year, Keywords
- Handle academic database exports (PubMed, Embase, etc.)

### Decision Categories
- **Include**: Clearly meets criteria, proceed to full-text review
- **Exclude**: Doesn't meet criteria, document reason
- **Uncertain**: Insufficient information, typically defaults to inclusion

### Common Exclusion Patterns
- Wrong population (age, condition mismatch)
- Wrong intervention (different treatment/dose)
- Wrong study type (editorials, case reports)
- Wrong outcomes (doesn't measure target endpoints)
- Language/publication restrictions

## LLM Integration Requirements

### Prompt Engineering Needs
- **Consistency**: Same criteria must yield same decisions across similar abstracts
- **Clarity**: Explicit instructions for include/exclude logic
- **Conservative Bias**: Prefer inclusion when uncertain (standard practice)
- **Structured Output**: Request consistent response format for parsing

### Expected LLM Response Format
```json
{
  "decision": "Include|Exclude|Uncertain",
  "reasoning": "Brief explanation of decision",
  "confidence": "High|Medium|Low"
}
```

### Error Handling Requirements
- **API Failures**: Retry with exponential backoff
- **Rate Limiting**: Batch processing with appropriate delays
- **Invalid Responses**: Request reformatted output, flag for manual review
- **Inconsistent Decisions**: Log potential issues for quality review

## Quality and Compliance

### Audit Trail Requirements
- Log all prompts sent to LLM
- Save complete LLM responses
- Record timestamps and model versions
- Enable decision reconstruction
- Support research transparency standards

### Performance Expectations
- **Accuracy**: Should match expert reviewer decisions >90% of time
- **Speed**: Process 100-1000 abstracts per hour (depending on API limits)
- **Consistency**: Same abstract with same criteria should yield same result
- **Transparency**: Every decision must be explainable

### Technical Constraints
- **Text Limits**: Abstract + prompt must fit within LLM context window
- **Cost Management**: Batch processing to optimize API usage
- **Rate Limits**: Respect provider API limitations
- **Data Security**: No persistent storage of research data

## Implementation Priority
1. **Core Function**: Reliable include/exclude decisions with reasoning
2. **User Experience**: Simple workflow from criteria input to results download
3. **Quality Assurance**: Consistent decisions and complete audit trail
4. **Scalability**: Handle typical systematic review volumes efficiently