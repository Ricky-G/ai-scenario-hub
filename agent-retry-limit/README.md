# Agent Retry Limit Scenario

## What This Demonstrates

This scenario shows how to implement retry limits in a multi-agent conversation flow using Semantic Kernel. When orchestrating multiple agents, you need mechanisms to handle failures and exit conversations gracefully. This example uses a mock authentication flow to demonstrate these concepts.

## The Problem

In multi-agent systems, you need to:
- Track failed attempts across agent interactions
- Detect when users are trying to circumvent the expected flow
- Terminate conversations when retry limits are exceeded
- Maintain state across multiple agent calls

## How It Works

### Agent Structure

The system has three agents:
1. **Intent Detection Agent** - Classifies user intent
2. **Authentication Agent** - Handles a mock authentication flow with math questions
3. **Orchestrator** - Manages state and enforces retry limits

### Key Implementation Details

**State Tracking**
```python
@dataclass
class ConversationContext:
    current_state: AgentState
    auth_attempts: int = 0  # Tracks failures
    auth_question_stage: int = 0
```

**Retry Logic**
- Each question allows 3 attempts
- Failed attempts increment `auth_attempts`
- At 3 failures, state changes to `TERMINAL`
- Conversation ends automatically

**Topic Change Detection**

The system uses AI to detect when users try to avoid the current flow:
```python
async def _check_topic_change(self, user_input: str) -> bool:
    # AI analyzes if user is answering the question or changing topic
```

If a topic change is detected, it counts as a failed attempt.

### Example Flow

```
User: check my balance
Bot: I can help you check your account balance. Let me verify your identity first.
     Please answer: What is 20 + 20?

User: I need something else     # <- Topic change detected
Bot: Please complete the authentication process first. What is 20 + 20? (Attempt 2/3)

User: help with another thing   # <- Another topic change
Bot: Please complete the authentication process first. What is 20 + 20? (Attempt 3/3)

User: forget it                 # <- Final attempt used
Bot: Maximum authentication attempts exceeded. This session has ended for security reasons.
[Session terminates]
```

## Technical Concepts Demonstrated

1. **State Machine Pattern**: Using enums to track conversation states
2. **Retry Counters**: Tracking attempts across agent interactions
3. **AI-Based Flow Detection**: Using LLM to detect conversation manipulation
4. **Graceful Termination**: Clean exit when limits are exceeded

## Running the Code

```bash
python app.py
```

The mock authentication uses simple math questions (20+20, 10+10) to simulate a multi-step verification process.

## Why This Matters

This pattern is useful for:
- Customer support escalation (limit attempts before human handoff)
- Form completion flows (prevent infinite loops)
- Security workflows (enforce attempt limits)
- Any multi-step process that needs failure handling

## Code Structure

- `IntentDetectionAgent`: Routes based on user intent
- `AuthenticationAgent`: Manages the mock auth flow
- `MultiAgentOrchestrator`: Coordinates agents and enforces limits
- `ConversationContext`: Maintains state across interactions

The retry limit logic is primarily in the orchestrator's `_handle_authentication()` method, which checks for topic changes and tracks failures.