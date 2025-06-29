# Semantic Kernel Multi-Agent Banking Assistant

A sophisticated multi-agent conversational AI system built with Microsoft's Semantic Kernel framework. This application demonstrates advanced agent orchestration, state management, and AI-powered conversation flows for a secure banking assistant scenario.

## 🤖 Agent Architecture

### 3 Specialized Agents Working Together

#### 1. **Intent Detection Agent**
- **Role**: Natural language understanding and intent classification
- **Capabilities**: 
  - Uses Azure OpenAI to analyze user requests
  - Classifies intents as account balance inquiries or other requests
  - Routes conversations to appropriate next steps

#### 2. **Authentication Agent** 
- **Role**: Multi-factor security verification
- **Features**:
  - Progressive security questioning system
  - Math-based challenge questions
  - 3-attempt security limit per question
  - AI-powered topic change detection to prevent authentication bypass

#### 3. **Multi-Agent Orchestrator**
- **Role**: Conversation flow management and state coordination
- **Responsibilities**:
  - Manages conversation state transitions
  - Coordinates between specialized agents
  - Maintains conversation history and context
  - Enforces security policies and session limits

## 🔄 Conversation Flow

```
User Input → Intent Detection → Authentication → Success/Termination
     ↓              ↓                ↓              ↓
[Any Request] → [Classify Intent] → [Security Q&A] → [Account Access]
```

### State Management
- **INTENT_DETECTION**: Initial user request analysis
- **AUTHENTICATION**: Security verification process  
- **SUCCESS**: Authenticated user with account access
- **TERMINAL**: Session ended (security failure or completion)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Azure OpenAI service account
- Azure OpenAI GPT-4 deployment

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/semantic-kernel-multi-agent.git
   cd semantic-kernel-multi-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.sample .env
   # Edit .env with your Azure OpenAI credentials
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## ⚙️ Environment Configuration

Create a `.env` file with the following required settings:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_GPT_4_1_DEPLOYMENT_NAME=your-gpt-4-deployment-name
```

### How to get these values:
1. **AZURE_OPENAI_ENDPOINT**: Found in Azure Portal → Your OpenAI Resource → Keys and Endpoint
2. **AZURE_OPENAI_API_KEY**: Found in Azure Portal → Your OpenAI Resource → Keys and Endpoint  
3. **AZURE_OPENAI_API_VERSION**: Use the latest stable version (2024-02-01 recommended)
4. **AZURE_OPENAI_GPT_4_1_DEPLOYMENT_NAME**: The deployment name you created for your GPT-4 model

## 🎯 Usage Example

```
=== Multi-Agent Banking Assistant ===
I can help you check your account balance.

You: I want to check my account balance
Assistant: I can help you check your account balance. Let me verify your identity first.

Please answer the following security question: What is 20 + 20?

You: 40
Assistant: Correct! Next question: What is 10 + 10?

You: 20
Assistant: Authentication successful! You can now access your account balance. Your current balance is $1,234.56.
```

## 🔒 Security Features

- **Progressive Authentication**: Multi-question verification system
- **Attempt Limits**: Maximum 3 attempts per security question
- **Topic Change Detection**: AI prevents authentication bypass attempts
- **Session Management**: Automatic termination on security violations
- **State Isolation**: Each conversation maintains independent security context

## 🛠️ Technical Features

### Built with Semantic Kernel
- **Agent Orchestration**: Seamless coordination between specialized agents
- **AI Integration**: Native Azure OpenAI connectivity
- **Function Calling**: Structured agent communication via kernel functions
- **Conversation Memory**: Persistent chat history throughout sessions

### Advanced AI Capabilities
- **Natural Language Understanding**: Intent classification using GPT-4
- **Context Awareness**: Maintains conversation state and history
- **Adaptive Responses**: Dynamic response generation based on user behavior
- **Topic Change Detection**: AI-powered conversation flow protection

## 📁 Project Structure

```
semantic-kernel-multi-agent/
├── app.py                 # Main application with multi-agent system
├── requirements.txt       # Python dependencies
├── .env.sample           # Environment variable template
├── .gitignore           # Git ignore rules
└── README.md            # This documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Microsoft Semantic Kernel**: For the powerful AI orchestration framework
- **Azure OpenAI**: For advanced language model capabilities
- **Python Community**: For the excellent ecosystem and libraries
