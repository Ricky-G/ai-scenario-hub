# Azure Text-to-Speech with SSML Fine-Tuning

## 🎛️ What This Demonstrates
This scenario shows how to use SSML (Speech Synthesis Markup Language) to fine-tune Azure Text-to-Speech voice characteristics beyond the default settings. Perfect for creating branded voice experiences or customizing speech for specific applications.

## 🎯 Use Cases
- **Customer Service Bots**: Calm, professional voice with slower speech and softer volume
- **Meditation Apps**: Gentle, soothing voice characteristics  
- **Educational Content**: Clear, measured speech with appropriate pacing
- **Brand Voice Consistency**: Maintain specific voice characteristics across all TTS interactions
- **Accessibility Applications**: Fine-tuned speech parameters for better comprehension

## � Technical Overview
Azure TTS works great with default settings, but SSML unlocks professional-grade voice customization:

- **Basic TTS**: `synthesizer.speak_text_async("Hello")` - uses default voice characteristics
- **SSML TTS**: Precise control over rate, pitch, volume, emphasis, breaks, and pronunciation

This example demonstrates the `CustomVoiceAgent` class that uses SSML `<prosody>` tags to create a custom voice profile with:
- Slightly slower speech (rate="0.9")
- Slightly higher pitch (pitch="+5%") 
- Softer volume (volume="soft")

## 🚀 Quick Start

### Prerequisites
- Azure Speech Services subscription
- Python 3.7+

### 1. Set up Azure credentials
Create a `.env` file:
```env
AZURE_SPEECH_KEY=your_speech_service_key
AZURE_SPEECH_REGION=your_region
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the demo
```bash
python app.py
```

### 4. Listen to the results
The script generates `test_response_*.wav` files demonstrating the custom voice characteristics.

## 💡 How to Use in Your Applications

### Basic Usage
```python
from app import CustomVoiceAgent

# Create agent with custom voice parameters
agent = CustomVoiceAgent()

# Generate speech with fine-tuned characteristics
agent.stream_to_wav("Welcome to our service!", "welcome.wav")
```

### Advanced SSML Customization
```python
# Modify the voice parameters in CustomVoiceAgent.__init__()
self.speech_rate = "0.8"      # Slower speech for clarity
self.pitch = "+10%"           # Higher pitch for friendliness  
self.volume = "soft"          # Softer volume for calm tone
```

## 🎚️ Voice Parameter Options

### Speech Rate
- `"0.5"` - Very slow (good for learning content)
- `"0.8"` - Slow (good for instructions)  
- `"1.0"` - Normal speed
- `"1.2"` - Fast (good for energetic content)
- `"2.0"` - Very fast

### Pitch Control
- `"low"`, `"medium"`, `"high"` - Keyword values
- `"-20%"` to `"+50%"` - Percentage adjustments
- `"-10Hz"` to `"+50Hz"` - Frequency adjustments

### Volume Control  
- `"soft"`, `"medium"`, `"loud"` - Keyword values
- `"-50%"` to `"+50%"` - Percentage adjustments
- `"0dB"` to `"+6dB"` - Decibel adjustments

## 🎯 SSML Features Demonstrated

### Core Prosody Control
```xml
<prosody rate="0.9" pitch="+5%" volume="soft">
    Your text with custom voice characteristics
</prosody>
```

### Additional SSML Capabilities
This example focuses on prosody, but SSML supports many other features:

- **Emphasis**: `<emphasis level="strong">important words</emphasis>`
- **Breaks**: `<break time="2s"/>` for pauses
- **Pronunciation**: `<phoneme>` for specific pronunciations
- **Voice Switching**: Multiple `<voice>` elements in one SSML document

## 🔧 Customization Guide

### For Different Applications

**Customer Service (Professional & Clear)**
```python
self.speech_rate = "0.9"      # Slightly slower for clarity
self.pitch = "medium"         # Neutral pitch
self.volume = "medium"        # Standard volume
```

**Meditation App (Calm & Soothing)**  
```python
self.speech_rate = "0.7"      # Slow, relaxed pace
self.pitch = "-5%"            # Slightly lower pitch
self.volume = "soft"          # Gentle volume
```

**Educational Content (Clear & Engaging)**
```python
self.speech_rate = "0.95"     # Slightly slower for comprehension
self.pitch = "+3%"            # Slightly higher for engagement
self.volume = "medium"        # Clear audibility
```

## 📁 File Structure
```
azure-speech-service-text-to-speech/
├── app.py              # Main CustomVoiceAgent implementation
├── requirements.txt    # Python dependencies
├── README.md          # This documentation
└── .env              # Azure credentials (create this)
```

## 🧪 What You'll Learn
- How to use SSML for professional voice customization
- Azure Speech Services SDK integration patterns
- Voice parameter optimization techniques
- Creating consistent branded voice experiences
- Industry-standard TTS practices

## 💰 Estimated Azure Costs
- Azure Speech Services: ~$4 per 1M characters
- This demo uses <1000 characters: ~$0.004

## 🔗 Related Resources
- [Azure Speech Services Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [SSML Reference](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup)
- [Voice Gallery](https://speech.microsoft.com/portal/voicegallery)
