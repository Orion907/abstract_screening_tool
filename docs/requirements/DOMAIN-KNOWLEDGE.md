# Domain Knowledge: Abstract Screening Implementation

## System Purpose
Automate systematic review abstract screening using PIC criteria. Process DistillerSR CSV exports to generate include/exclude decisions with reasoning for exclusions based on PIC criteria.

## Input Specification
**CSV Structure (DistillerSR Export):**
- Required columns: Reference ID, Title, Abstract text
- Expected volume: 1,000-10,000+ abstracts per batch

## Screening Criteria Framework Implementation
**Primary PIC Components:**
- **Population**: Patient/subject demographics, conditions, settings
- **Intervention**: Specific therapies, procedures, exposures
- **Comparator**: Control or alternative treatments

**Additional Exclusion Criteria:**
- Geographic restrictions (e.g., studies in developing countries)
- Study design limitations
- Language restrictions
- Publication date ranges
- Other protocol-specific exclusions

**Prompt Requirements:**
- Convert all screening criteria (PIC + additional) to explicit include/exclude instructions
- Handle incomplete/ambiguous criteria gracefully
- Accept Word document paste inputs (formatting issues)
- Support custom prompts as alternative to structured criteria

## LLM Integration Specifications

### Response Format
```json
{
  "decision": "Include|Exclude",
  "reasoning": "Brief explanation for exclusion only (empty for inclusions)"
}
```

### Decision Logic
- **Include**: Meets all screening criteria or insufficient information to exclude
  - No reasoning required for inclusion decisions
  - Conservative bias toward inclusion when uncertain
- **Exclude**: Clearly violates any screening criteria (PIC or additional)
  - Reasoning required explaining which specific criteria were violated
- **Reasoning**: Must explicitly reference the violated criteria in explanation

### Common Exclusion Patterns
- Wrong population (age, condition mismatch)
- Wrong intervention (different treatment/dose)
- Wrong or missing comparator
- Geographic restrictions (e.g., developing country studies)
- Study design incompatible with review requirements
- Language or publication date restrictions

## Output Requirements
**CSV Columns:**
- Reference ID
- Title
- Decision (Include|Exclude)
- Reasoning (Explanation for exclusions based on any violated criteria, empty for inclusions)

## Technical Constraints
- **Context Limits**: Abstract + prompt must fit LLM context window
- **Error Handling**: Retry API failures, handle rate limits, flag invalid responses
- **Audit Trail**: Log prompts, responses, timestamps, model versions
- **Performance**: >90% accuracy vs expert reviewers, 100-1000 abstracts/hour
- **Security**: No persistent storage of research data

## Implementation Priority
1. Reliable screening decisions with reasoning for exclusions based on all criteria
2. DistillerSR CSV input/output workflow
3. Complete audit trail
4. Batch processing efficiency