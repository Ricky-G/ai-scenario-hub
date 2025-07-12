# GitHub Copilot Instructions

## Repository Context

This repository contains multi-agent orchestration examples using Microsoft's Semantic Kernel framework. Each scenario demonstrates specific patterns for coordinating multiple AI agents.

## Code Style & Patterns

**Python Conventions:**
- Use type hints for all function parameters and return values
- Follow PEP 8 naming conventions
- Use dataclasses for state management
- Implement async/await patterns for agent interactions

**Agent Architecture:**
- Each scenario should have separate agent classes for distinct responsibilities
- Use an orchestrator pattern to coordinate multiple agents
- Implement proper state management across agent interactions
- Include error handling and graceful degradation

**File Structure:**
- Each scenario in its own folder with descriptive name
- `app.py` as the main entry point
- `README.md` with technical implementation details
- Follow existing folder structure patterns

## Semantic Kernel Specifics

Use documenation from the offical site https://learn.microsoft.com/en-us/semantic-kernel/overview/

**Agent Implementation:**
- Use Semantic Kernel's chat completion service
- Implement proper prompt templates and function calling
- Use kernel plugins for reusable functionality
- Follow SK's async patterns

**Configuration:**
- Use environment variables for Azure OpenAI configuration
- Support the existing `.env` pattern
- Handle missing configuration gracefully

## Documentation Standards

**Scenario READMEs:**
- Lead with the technical problem being solved
- Include implementation architecture overview
- Provide code examples for key concepts
- List prerequisites and setup instructions
- Keep language technical and developer-focused

**Code Comments:**
- Document complex orchestration logic
- Explain retry mechanisms and state transitions
- Comment on AI prompt strategies

## Testing & Validation

- Test scenarios end-to-end with real Azure OpenAI calls
- Validate error handling paths
- Ensure graceful degradation when APIs are unavailable
- Test state management across multiple agent interactions

## Contribution Guidelines

When suggesting new scenarios:
- Focus on real-world multi-agent orchestration patterns
- Demonstrate specific technical challenges and solutions
- Avoid duplicating existing scenario concepts
- Include proper error handling and retry logic
