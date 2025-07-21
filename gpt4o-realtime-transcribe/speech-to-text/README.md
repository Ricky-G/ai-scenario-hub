# Azure OpenAI GPT-4o Real-time Speech Transcription

## 🎯 What This Does
Real-time speech-to-text transcription using Azure OpenAI's GPT-4o transcribe model with WebSocket streaming.

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Azure credentials
Edit `.env` file with your Azure OpenAI credentials:
```env
AZURE_OPENAI_KEY=your_azure_openai_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

### 3. Run the transcription
```bash
python app.py
```

### 4. Start speaking
- The app will show available audio input devices
- Start speaking into your microphone
- See real-time transcription in your terminal
- Press `Ctrl+C` to stop

## 🎤 Features

- **Real-time Processing** - Instant speech-to-text with minimal latency
- **WebSocket Streaming** - Continuous audio streaming to Azure OpenAI
- **Voice Activity Detection** - Automatic detection of speech start/stop
- **Noise Reduction** - Built-in audio preprocessing for better accuracy
- **Multi-device Support** - Choose from available microphone inputs

## 🔧 Configuration Options

The app uses GPT-4o transcription with these settings:

```python
# Audio quality
SAMPLE_RATE = 24000      # 24kHz for optimal quality
FORMAT = pyaudio.paInt16 # 16-bit PCM audio
CHANNELS = 1             # Mono audio

# Transcription settings
model = "gpt-4o-transcribe"           # Latest transcription model
noise_reduction = "near_field"        # Optimized for close microphones
language = "en"                       # English (change as needed)
```

## 📋 Requirements

- **Azure OpenAI Account** - With GPT-4o access
- **Python 3.8+** - With pip package manager
- **Microphone** - Any audio input device
- **Internet Connection** - For real-time streaming

## 💡 Use Cases

- **Live Meeting Transcription** - Real-time notes during calls
- **Voice-to-Text Input** - Convert speech to written text
- **Accessibility Tool** - Audio content transcription
- **Content Creation** - Quick voice note transcription

## 🔍 How It Works

1. **WebSocket Connection** - Establishes secure connection to Azure OpenAI
2. **Audio Capture** - Continuously captures microphone input
3. **Streaming Upload** - Sends audio chunks in real-time via WebSocket
4. **Live Transcription** - Receives and displays transcribed text instantly
5. **Session Management** - Handles connection lifecycle and errors

## ⚡ Performance

- **Latency**: ~200-500ms from speech to text
- **Accuracy**: Leverages GPT-4o's advanced language understanding
- **Throughput**: Continuous streaming with no interruptions
- **Quality**: 24kHz audio ensures optimal transcription accuracy

## 🛠️ Troubleshooting

**No audio input detected:**
- Check microphone permissions
- Verify audio device is working
- Try selecting different input device

**Connection errors:**
- Verify Azure OpenAI credentials in `.env`
- Check internet connection
- Ensure GPT-4o access is enabled

**Poor transcription quality:**
- Speak clearly and at normal pace
- Reduce background noise
- Check microphone positioning
