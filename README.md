# Semantic Kernel Multi-Agent Scenarios

Code examples demonstrating multi-agent orchestration patterns using Microsoft's Semantic Kernel framework.

## Scenarios

### 1. [Agent Retry Limit](./agent-retry-limit/)

Implements retry limits and graceful termination in multi-agent conversations using a mock authentication flow.

**Technical Features:**
- Retry counters across agent interactions
- AI-based topic change detection
- State machine pattern with graceful termination
- Cross-agent state management

**Implementation:** Intent detection → Authentication flow → Orchestrator with retry limits

[View implementation details](./agent-retry-limit/README.md)

## Setup

**Prerequisites:**
- Python 3.8+
- Azure OpenAI account with GPT-4 deployment

**Installation:**
```bash
git clone https://github.com/ricky-g/semantic-kernal-multi-agen-scenarios.git
cd semantic-kernal-multi-agen-scenarios
pip install -r requirements.txt
```

**Configuration:**
```bash
cp .env.sample .env
# Edit .env with your Azure OpenAI credentials
```

**Run scenario:**
```bash
cd agent-retry-limit
python app.py
```

## Environment Configuration

Required `.env` variables:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_GPT_4_1_DEPLOYMENT_NAME=your-gpt4-deployment-name
```

## Repository Structure

```
semantic-kernal-multi-agen-scenarios/
├── agent-retry-limit/          
│   ├── app.py                  
│   └── README.md              
├── requirements.txt           
├── .env.sample               
└── README.md                 
```

## Contributing

To add a new scenario:
1. Create folder with descriptive name
2. Include `app.py` with implementation
3. Add `README.md` with technical details
4. Follow existing code patterns

## Resources

- [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)
- [Semantic Kernel GitHub](https://github.com/microsoft/semantic-kernel)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service)