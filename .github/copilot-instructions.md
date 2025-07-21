# GitHub Copilot Instructions

## Repository Context

This repository contains AI and Speech Services scenarios for experimentation and learning. Each scenario provides complete working code for common AI patterns including speech processing, real-time transcription, and agent orchestration.

## Code Style & Standards

**Python Conventions:**
- Use type hints for all function parameters and return values
- Follow PEP 8 naming conventions
- Implement async/await patterns for AI service interactions
- Include comprehensive error handling

**Scenario Architecture:**
- Each scenario is self-contained in its own folder
- Use `app.py` as the main entry point
- Include detailed documentation and examples
- Follow existing folder structure patterns

**File Structure:**
```
scenario-name/
├── app.py                 # Main application
├── README.md              # Documentation & setup
├── requirements.txt       # Dependencies
└── .env                   # Configuration template
```

## AI Service Integration

**Azure Services:**
- Use environment variables for Azure credentials
- Handle authentication and API errors gracefully
- Follow Azure SDK best practices
- Support the existing `.env` pattern

**Speech Services:**
- Use SSML for consistent voice characteristics
- Implement proper audio streaming patterns
- Handle real-time processing efficiently

**Agent Orchestration:**
- Use Semantic Kernel for multi-agent scenarios
- Implement proper state management
- Include retry mechanisms and graceful termination

## Documentation Standards

**Scenario READMEs:**
- Lead with the problem being solved
- Include clear setup instructions
- Provide working code examples
- List prerequisites and estimated costs
- Keep language accessible for learning

**Code Comments:**
- Document complex AI integration logic
- Explain SSML and voice parameter choices
- Comment on retry mechanisms and error handling

## Testing & Validation

- Test scenarios with real Azure services
- Validate error handling and edge cases
- Ensure consistent performance across different inputs
- Test authentication and configuration scenarios

## Contribution Guidelines

When adding new scenarios:
- Focus on practical AI implementation patterns
- Demonstrate real-world use cases
- Include complete working examples
- Ensure scenarios are self-contained and well-documented
