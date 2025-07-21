# AI Scenario Hub 🤖

Code samples for Azure AI and Speech Services.
Each folder contains a working example with setup instructions.

> **Note:** These implementations are designed for development and testing environments. Review security configurations before production deployment.

## Overview

Code samples for Azure AI service integrations. Each folder contains a standalone implementation
that demonstrates how to solve specific problems with Azure OpenAI, Speech Services, and agent orchestration.

### What's included:
• **Working code examples** - Clone and run implementations
• **Configuration templates** - Environment setup for Azure services  
• **Implementation docs** - Technical details and API usage
• **Common patterns** - Reusable approaches for typical scenarios

## Available Scenarios

### Speech & Audio Processing

| Scenario | Implementation | Status | Technical Features |
|----------|------------|---------|---------------|
| [Text-to-Speech Voice Consistency](./text-to-speech/) | Solves voice parameter drift in Azure TTS conversations | ✅ Ready | SSML parameter locking, prosody control, consistent audio output |
| [Real-time Speech Transcription](./gpt4o-realtime-transcribe/) | WebSocket-based real-time speech-to-text with GPT-4o | ✅ Ready | WebSocket streaming, audio capture, real-time processing pipeline |

### AI Agent Orchestration

| Scenario | Implementation | Status | Technical Features |
|----------|------------|---------|---------------|
| [Semantic Kernel Multi-Agent Retry Limit](./semantic-kernel-agent-retry-limit/) | Multi-agent conversation flow with retry logic and termination | ✅ Ready | State management, retry counters, conversation orchestration |

### Contributing scenarios:
Submit technical scenarios via [issues](https://github.com/Ricky-G/ai-scenario-hub/issues) with implementation requirements.

## Setup Instructions

### 1. Repository setup
```bash
git clone https://github.com/Ricky-G/ai-scenario-hub.git
cd ai-scenario-hub
```

### 2. Scenario selection
```bash
cd <scenario-directory>
```

### 3. Environment configuration
```bash
# Configure Azure credentials in .env file
cp .env.template .env  # Edit with your service keys
pip install -r requirements.txt
python app.py
```

## Dependencies

**Required services:**
• **Azure Subscription** - [Setup guide](https://azure.microsoft.com/free/)
• **Azure OpenAI** - GPT-4/GPT-4o access required
• **Azure Speech Services** - For TTS scenarios

**Development environment:**
• **Python 3.8+** - [Download](https://www.python.org/downloads/)
• **Azure CLI** - [Installation](https://learn.microsoft.com/cli/azure/install-azure-cli)

## Technology Stack

**AI Services:**
• Azure OpenAI (GPT-4, GPT-4o)
• Azure Speech Services
• Semantic Kernel SDK

**Infrastructure:**
• WebSocket connections
• SSML markup
• Audio processing (PyAudio)
• Async/await patterns

## Repository Structure

```
scenario-name/
├── README.md              # Implementation guide and API docs
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
└── .env                   # Service configuration (template)
```

## Development Notes

**Implementation patterns:**
• Each scenario is self-contained with minimal dependencies
• Configuration via environment variables
• Error handling and logging included
• Async patterns for service calls

**Service integration:**
• Authentication via Azure SDK patterns
• Retry logic for transient failures  
• Resource cleanup and connection management
• Environment-specific configuration

## Contributing

**Adding scenarios:**
1. Fork repository
2. Create scenario directory with required structure
3. Include comprehensive README with technical details
4. Test with actual Azure services
5. Submit pull request

**Code standards:**
• Python type hints required
• Error handling for service calls
• Environment configuration patterns
• Documentation for public APIs

## Support

**Technical issues:**
• [GitHub Issues](https://github.com/Ricky-G/ai-scenario-hub/issues) - Bug reports and feature requests
• [Discussions](https://github.com/Ricky-G/ai-scenario-hub/discussions) - Implementation questions

**Security:**
• Review [SECURITY.md](./SECURITY.md) for vulnerability reporting
• Validate configurations before production deployment

## License

MIT License - Open source usage permitted.