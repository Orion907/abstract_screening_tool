# Domain Knowledge: Abstract Screening Implementation

## System Purpose
Automate systematic review abstract screening using PIC criteria. Process DistillerSR CSV exports to generate include/exclude decisions with reasoning based on PIC criteria.

## Input Specification
**CSV Structure (DistillerSR Export):**
- Required columns: Reference ID, Title, Abstract text
- Expected volume: 1,000-10,000+ abstracts per batch

## PIC Framework Implementation
**Criteria Components:**
- **Population**: Patient/subject demographics, conditions, settings
- **Intervention**: Specific therapies, procedures, exposures
- **Comparator**: Control or alternative treatments

**Prompt Requirements:**
- Convert PIC criteria to explicit include/exclude instructions
- Handle incomplete/ambiguous criteria gracefully
- Accept Word document paste inputs (formatting issues)
- Support custom prompts as alternative to structured PIC

## LLM Integration Specifications

### Response Format
```json
{
  "decision": "Include|Exclude",
  "reasoning": "Brief explanation based on PIC criteria"
}
```

### Decision Logic
- **Include**: Meets PIC criteria or insufficient information to exclude
- **Exclude**: Clearly violates PIC criteria
- **Bias**: Conservative toward inclusion when uncertain
- **Reasoning**: Must explicitly reference PIC criteria in explanation

### Common Exclusion Patterns
- Wrong population (age, condition mismatch)
- Wrong intervention (different treatment/dose)
- Wrong or missing comparator
- Study type incompatible with intervention comparison

## Output Requirements
**CSV Columns:**
- Reference ID
- Title
- Decision (Include|Exclude)
- Reasoning (PIC-based explanation)

## Technical Constraints
- **Context Limits**: Abstract + prompt must fit LLM context window
- **Error Handling**: Retry API failures, handle rate limits, flag invalid responses
- **Audit Trail**: Log prompts, responses, timestamps, model versions
- **Performance**: >90% accuracy vs expert reviewers, 100-1000 abstracts/hour
- **Security**: No persistent storage of research data

## Implementation Priority
1. Reliable PIC-based decisions with reasoning
2. DistillerSR CSV input/output workflow
3. Complete audit trail
4. Batch processing efficiency