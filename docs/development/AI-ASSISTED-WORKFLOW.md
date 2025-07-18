# AI-Assisted Development Workflow

## Overview
This document defines the step-by-step process for developing the Abstract Screening Tool using AI code generation while maintaining tight control and learning software engineering principles.

## Development Phases

### Phase 1: Specification and Design
**Goal**: Define what to build before building it

#### Step 1.1: Create Module Specification
For each module in the architecture:

1. **Copy template**: Use `module-specification-template.md`
2. **Define purpose**: Clear, single responsibility
3. **Specify interfaces**: All public functions with exact signatures
4. **Define data contracts**: Input/output types and validation
5. **Document dependencies**: Internal and external
6. **Review and approve**: Manual review before any implementation

**Deliverable**: Complete module specification document

#### Step 1.2: Create Interface Contracts
For complex modules:

1. **Copy template**: Use `interface-contracts-template.md`
2. **Detail function signatures**: Exact type hints and docstrings
3. **Define error handling**: All exceptions and recovery strategies
4. **Specify test requirements**: What must be tested
5. **Create usage examples**: How the interface should be used

**Deliverable**: Interface contracts document

#### Step 1.3: Design Review
Before any code:

1. **Architecture consistency**: Does this fit the overall design?
2. **Dependency check**: Are all dependencies available?
3. **Interface review**: Are the contracts clear and complete?
4. **Test strategy**: Can this be properly tested?

**Gate**: Must pass review before proceeding to implementation

### Phase 2: Implementation Authorization

#### Step 2.1: Implementation Planning
For each module:

1. **Break down work**: Identify individual functions/classes
2. **Prioritize order**: Start with data models, then core logic
3. **Identify risks**: What could go wrong?
4. **Plan testing**: How will you verify it works?

#### Step 2.2: AI Prompt Preparation
Before generating code:

1. **Context preparation**: Gather all relevant specifications
2. **Clear instructions**: Exactly what to implement
3. **Constraint specification**: What patterns to follow
4. **Quality criteria**: How to judge success

**Template AI Prompt**:
```
I need you to implement [specific function/class] according to the following specification:

**Module**: [module name and purpose]
**Interface Contract**: [paste relevant interface contract]
**Dependencies**: [list available imports]
**Constraints**: 
- Follow the interface contract exactly
- Use error handling patterns from [error handling doc]
- Include comprehensive docstrings
- Add type hints for all parameters and returns

**Implementation Requirements**:
[specific details about what to implement]

Please implement only the specified component and include basic unit tests.
```

### Phase 3: Controlled Implementation

#### Step 3.1: Incremental Development
**Rule**: Implement one module at a time, bottom-up

**Order of Implementation**:
1. **Data Models** (`data/models/`) - Foundation types
2. **Utilities** (`utils/`) - Supporting functions
3. **Data Processing** (`data/processors/`) - Core data handling
4. **Core Logic** (`core/`) - Business logic
5. **LLM Integration** (`llm/`) - External services
6. **UI Components** (`ui/`) - User interface

#### Step 3.2: Function-Level Authorization
For each function:

1. **Review generated code**: Does it match the specification?
2. **Check dependencies**: Are imports correct and available?
3. **Validate error handling**: Are exceptions handled properly?
4. **Test the implementation**: Run basic tests
5. **Authorize or reject**: Clear decision before moving on

**Authorization Checklist**:
- [ ] Matches interface contract exactly
- [ ] Follows naming conventions
- [ ] Includes proper error handling
- [ ] Has comprehensive docstrings
- [ ] Includes type hints
- [ ] Basic tests pass
- [ ] No obvious security issues

#### Step 3.3: Integration Testing
After each module:

1. **Unit tests**: All functions work in isolation
2. **Integration tests**: Module works with dependencies
3. **Interface validation**: Public API works as specified
4. **Error propagation**: Errors are handled appropriately

### Phase 4: Quality Assurance

#### Step 4.1: Code Review Process
For each completed module:

1. **Specification compliance**: Does it meet the original spec?
2. **Code quality**: Is it readable and maintainable?
3. **Test coverage**: Are all paths tested?
4. **Documentation**: Is it properly documented?

#### Step 4.2: Learning Review
After each module:

1. **What patterns were used**: Observer, Strategy, Factory, etc.?
2. **What challenges arose**: How were they solved?
3. **What would you do differently**: Lessons learned
4. **How to improve**: Process refinements

**Learning Log Template**:
```
## Module: [name]
**Patterns Used**: [design patterns applied]
**Challenges**: [problems encountered and solutions]
**Key Learnings**: [software engineering principles learned]
**Process Improvements**: [how to do it better next time]
```

## AI Interaction Guidelines

### Effective Prompting for Code Generation

#### For Data Models:
```
Create a Pydantic model for [entity] with the following requirements:
- [specific fields and types]
- [validation rules]
- [methods needed]
- Include comprehensive docstrings and type hints
```

#### For Business Logic:
```
Implement [function name] that [specific purpose]:
- Input: [exact parameters and types]
- Output: [exact return type]
- Error handling: [specific exceptions to raise]
- Dependencies: [available imports]
- Follow the interface contract: [paste contract]
```

#### For Tests:
```
Create comprehensive unit tests for [function/class]:
- Test all normal operations
- Test all error conditions
- Test edge cases: [specific cases]
- Use pytest and these fixtures: [available fixtures]
```

### Quality Control for AI-Generated Code

#### Immediate Checks:
1. **Syntax**: Does it run without syntax errors?
2. **Imports**: Are all dependencies available?
3. **Types**: Do type hints match the interface?
4. **Docstrings**: Are they complete and accurate?

#### Deeper Review:
1. **Logic**: Does the implementation make sense?
2. **Edge cases**: Are they handled properly?
3. **Performance**: Is it efficient enough?
4. **Security**: Are inputs validated properly?

## Common Pitfalls and Solutions

### Pitfall 1: Over-Generating
**Problem**: AI generates more than requested
**Solution**: Be very specific about scope in prompts

### Pitfall 2: Specification Drift
**Problem**: Implementation doesn't match specification
**Solution**: Always reference the original spec in prompts

### Pitfall 3: Missing Error Handling
**Problem**: Happy path only, no error cases
**Solution**: Explicitly request error handling in every prompt

### Pitfall 4: Poor Test Coverage
**Problem**: Tests don't cover edge cases
**Solution**: Specify exact test scenarios needed

## Success Metrics

### Technical Metrics:
- **Specification Compliance**: 100% of interfaces match contracts
- **Test Coverage**: >90% line coverage
- **Error Handling**: All error paths tested
- **Documentation**: All public APIs documented

### Learning Metrics:
- **Pattern Recognition**: Can identify design patterns used
- **Architecture Understanding**: Can explain module interactions
- **Problem Solving**: Can debug issues independently
- **Process Improvement**: Can refine development workflow

## Tools and Environment

### Required Tools:
- **VSCode**: With Python and GitHub Copilot extensions
- **Python 3.8+**: With virtual environment
- **pytest**: For testing
- **mypy**: For type checking
- **black**: For code formatting

### Recommended Workflow:
1. **Write specification** → Review → Approve
2. **Generate code** → Test → Review → Approve
3. **Integration test** → Document → Commit
4. **Learning review** → Process improvement

This workflow ensures you maintain control while learning fundamental software engineering practices through hands-on implementation.