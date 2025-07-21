# GPT-4o Real-time Conversation with Text-to-Speech

## 🎯 What This Demonstrates
This scenario shows how to combine GPT-4o's real-time conversational API with Azure Speech Services to create a voice-enabled AI assistant. You type messages, GPT-4o responds intelligently, and the responses are automatically converted to natural speech.

## 🚀 Architecture Overview
- **GPT-4o Real-time API**: Conversational AI via WebSocket streaming
- **Azure Speech Services TTS**: Convert AI responses to natural speech  
- **Real-time Pipeline**: Text input → AI processing → Speech output
- **Background Processing**: TTS queue system for smooth audio playback

## 🎯 Use Cases
- **Voice Assistants**: Natural conversation with speech output
- **Accessibility Tools**: Text-to-speech for AI interactions
- **Educational Apps**: Interactive learning with spoken responses
- **Customer Service**: AI agents that can "speak" to users
- **Prototyping**: Quick voice interface testing for AI applications

## 🔧 Technical Features

### GPT-4o Real-time Conversation
- **WebSocket Streaming**: Real-time bidirectional communication
- **Conversational Context**: Maintains conversation history and context
- **Configurable Personality**: Customizable AI instructions and behavior
- **Response Streaming**: See AI responses as they're generated

### Azure Speech Services Integration
- **Natural Voices**: Uses Azure Neural voices (en-US-AriaNeural)
- **SSML Control**: Fine-tuned speech characteristics
- **Background Processing**: Non-blocking TTS with queue system
- **Audio Playback**: Integrated pygame for seamless audio playback

## 🚀 Quick Start

### Prerequisites
- Azure OpenAI subscription with GPT-4o access
- Azure Speech Services subscription
- Python 3.8+

### 1. Set up Azure credentials
Create a `.env` file:
```env
# Azure OpenAI (for GPT-4o conversation)
AZURE_OPENAI_KEY=your_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Azure Speech Services (for TTS)
AZURE_SPEECH_KEY=your_speech_key
AZURE_SPEECH_REGION=your_region
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the conversation demo
```bash
python app.py
```

### 4. Start chatting!
- Type your messages when prompted
- GPT-4o will respond with text
- Responses are automatically converted to speech
- Type 'quit' to exit

## 💬 Example Conversation Flow

```
Your message: Tell me a joke about programmers
👤 You: Tell me a joke about programmers
🤖 GPT-4o: Why do programmers prefer dark mode? 
Because light attracts bugs! 🐛

🔊 Speaking response...
🔊 Speech completed

Your message: That's funny! Tell me about AI
👤 You: That's funny! Tell me about AI  
🤖 GPT-4o: I'm glad you enjoyed that! AI, or Artificial Intelligence, 
is like giving computers the ability to think and learn...

🔊 Speaking response...
🔊 Speech completed
```

## 🎛️ Customization Options

### Conversation Personality
Edit the session configuration in `on_open()`:
```python
"instructions": "You are a helpful AI assistant. Keep responses conversational and engaging."
```

### Voice Characteristics
Modify the TTS voice in `__init__()`:
```python
# Change voice model
self.speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"  # Female
# Or
self.speech_config.speech_synthesis_voice_name = "en-US-GuyNeural"    # Male
```

### Speech Parameters
Customize SSML in `create_response_ssml()`:
```python
# Slower, calmer speech
<prosody rate="0.9" pitch="medium" volume="soft">

# Faster, energetic speech  
<prosody rate="1.2" pitch="+5%" volume="medium">
```

### Response Behavior
Adjust GPT-4o parameters:
```python
"temperature": 0.8,              # Creativity (0.0-2.0)
"max_response_output_tokens": 4096,  # Response length
```

## 🏗️ Code Architecture

### Main Components

**GPT4oConversationAgent Class**
- Manages WebSocket connection to GPT-4o
- Handles TTS queue and audio playback
- Coordinates conversation flow

**WebSocket Event Handlers**
- `on_open()`: Session configuration
- `on_message()`: Process AI responses  
- `on_error()`: Error handling
- `on_close()`: Cleanup

**TTS Pipeline**
- `speak_response()`: Convert text to speech
- `tts_worker()`: Background TTS processing
- `create_response_ssml()`: SSML generation

### Data Flow
```
User Input → GPT-4o API → Text Response → TTS Queue → Audio Playback
```

## 🎯 Learning Objectives
- **Real-time AI APIs**: WebSocket communication with GPT-4o
- **Asynchronous Processing**: Background TTS with queue management
- **Audio Integration**: pygame for audio playback in Python
- **Azure Services Integration**: Combining OpenAI + Speech Services
- **Conversation Design**: Building natural AI interactions

## 🔧 Advanced Features

### Adding Voice Input
You could extend this to include speech-to-text:
```python
# Add microphone input → GPT-4o transcription → conversation
# Create full voice-to-voice AI assistant
```

### Multi-language Support
```python
# Configure for different languages
"input_audio_transcription": {
    "model": "whisper-1",
    "language": "es"  # Spanish
}
```

### Conversation History
```python
# Save and restore conversation context
# Implement conversation memory persistence
```

## 📁 File Structure
```
text-to-speech/
├── app.py              # Main conversation agent
├── requirements.txt    # Python dependencies  
├── README.md          # This documentation
└── .env              # Azure credentials (create this)
```

## 🧪 Demo Conversation Ideas
Try these prompts to test the system:

**Fun & Creative**
- "Tell me a joke about AI"
- "Create a short story about a robot"
- "What's your favorite color and why?"

**Educational**  
- "Explain machine learning in simple terms"
- "How does the internet work?"
- "What's the difference between AI and ML?"

**Practical**
- "Help me plan a weekend trip"
- "What's a good recipe for dinner?"
- "Give me tips for public speaking"

## 💰 Estimated Azure Costs
- **Azure OpenAI GPT-4o**: ~$30 per 1M input tokens, ~$60 per 1M output tokens
- **Azure Speech Services TTS**: ~$4 per 1M characters
- **This demo**: Approximately $0.01-0.05 per conversation (depending on length)

## 🔗 Related Resources
- [Azure OpenAI Real-time API Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Azure Speech Services Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [GPT-4o Real-time API Reference](https://platform.openai.com/docs/guides/realtime)

## 🚨 Important Notes

**Real-time vs Transcription APIs**
- This uses GPT-4o **conversation** API (bidirectional chat)
- Different from GPT-4o **transcription** API (speech-to-text only)
- Enables full conversational AI with context and memory

**Audio Requirements**
- Requires speakers or headphones for audio output
- pygame handles audio playback automatically
- Temporary WAV files are created and cleaned up automatically
