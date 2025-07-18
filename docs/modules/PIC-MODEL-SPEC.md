# Module Specification: PIC Criteria Data Model
## File: `data/models/pic.py`

## What This Module Does (In Plain English)
This module creates a "container" to hold PIC criteria that users type into the app. Think of it like a form with specific fields that we want to validate and use throughout the program.

## What We Need to Store
Based on your requirements documents, we need to store:
- **Population**: Who are we studying? (e.g., "adults with diabetes")
- **Intervention**: What treatment are we testing? (e.g., "insulin therapy") 
- **Comparator**: What are we comparing it to? (e.g., "standard care")
- **Additional inclusion criteria**: Other requirements (optional)
- **Additional exclusion criteria**: Other restrictions (optional)

## Software Terms We'll Learn
- **Data Model**: A structure that defines what information we store and how
- **Validation**: Checking that the data is correct (e.g., not empty when required)
- **Pydantic**: A Python library that makes creating data models easy
- **Type Hints**: Telling Python what kind of data each field should be (text, number, etc.)

## What the Code Should Look Like (High Level)
```python
# This creates a "template" for PIC criteria
class PICCriteria:
    population: [some text that can't be empty]
    intervention: [some text that can't be empty] 
    comparator: [some text that can't be empty]
    inclusion_criteria: [optional list of additional criteria]
    exclusion_criteria: [optional list of additional criteria]
    
    # Plus some helper methods:
    # - Check if the criteria are complete
    # - Convert to text for the LLM
    # - Validate that required fields aren't empty
```

## What We Want to Be Able to Do
```python
# Create PIC criteria from user input
pic = PICCriteria(
    population="adults with Type 2 diabetes",
    intervention="metformin 500mg daily",
    comparator="placebo"
)

# Check if it's valid
if pic.is_complete():
    # Use it to generate prompts
    prompt_text = pic.to_prompt_text()
    
# Handle errors gracefully
try:
    pic = PICCriteria(population="", intervention="test", comparator="test")
except ValidationError:
    print("Population cannot be empty!")
```

## Questions to Answer Together
1. **Should inclusion/exclusion criteria be required or optional?**
   - From your docs, it seems optional (users can paste from Word docs that might not have them)

2. **What happens if someone pastes messy text with extra spaces?**
   - Should we clean it up automatically?

3. **How long can each field be?**
   - Do we need limits to prevent extremely long inputs?

4. **What validation rules do we need?**
   - Just "not empty" for required fields, or more sophisticated checks?

## Next Steps (We'll Do This Together)
1. **Define the exact fields** we need
2. **Choose validation rules** that make sense  
3. **Write the code** using Pydantic (I'll explain as we go)
4. **Create simple tests** to make sure it works
5. **Learn terminology** naturally as we encounter it

## Learning Goals for This Module
By the time we're done, you'll understand:
- What a "data model" is and why we need them
- How validation works and why it's important
- Basic Python type hints (str, Optional, List)
- How to structure code for reusability
- What makes code "testable"

---

## Your Task (If You're Ready)
**Option 1**: Answer the questions above based on your domain knowledge
**Option 2**: Say "let's build it together" and I'll walk you through each decision

**Either way, we'll learn the terminology as we go, and I'll explain every software engineering concept when we encounter it!**