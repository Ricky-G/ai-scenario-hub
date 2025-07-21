#!/usr/bin/env python3
"""
Azure TTS with SSML Fine-Tuning

This demonstrates how to use SSML (Speech Synthesis Markup Language) to fine-tune 
voice characteristics beyond the default settings.

WHAT THIS SHOWS:
- Using SSML for precise voice control (speed, pitch, volume)
- Fine-tuning voice characteristics for specific use cases
- Going beyond basic text-to-speech with advanced prosody control

THE APPROACH:
- Use SSML markup for explicit voice parameter control
- Set consistent prosody values across all TTS calls
- Demonstrate professional voice customization techniques

WHY USE SSML FOR VOICE FINE-TUNING:
==================================

🔧 BASIC APPROACH (default voice settings):
    speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
    synthesizer.speak_text_async("Hello there!")
    
    LIMITATIONS:
    - Uses default voice characteristics
    - No control over speech rate, pitch, or volume
    - Limited customization options
    - Good for basic TTS, but not for fine-tuned applications

✨ SSML APPROACH (fine-tuned control):
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
        <voice name="en-US-AriaNeural">
            <prosody rate="0.9" pitch="+5%" volume="soft">
                Hello there!
            </prosody>
        </voice>
    </speak>
    
    ADVANTAGES:
    - Precise control over speech characteristics
    - Fine-tune rate, pitch, and volume to exact specifications
    - Create consistent branded voice experiences
    - Professional-grade voice customization

SSML = Speech Synthesis Markup Language
- XML-based markup for advanced speech control
- Industry standard for professional TTS applications
- Enables voice branding and consistent user experiences
- Supports advanced features like emphasis, breaks, and pronunciation
"""

import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CustomVoiceAgent:
    """
    ✨ SSML-powered voice agent with fine-tuned characteristics
    """
    
    def __init__(self):
        # Configure Azure Speech Service
        self.speech_config = SpeechConfig(
            subscription=os.getenv("AZURE_SPEECH_KEY"),
            region=os.getenv("AZURE_SPEECH_REGION")
        )
        
        # 🎛️ CUSTOMIZATION: Set specific voice parameters for your use case
        # These values define the "personality" of your voice agent
        # Adjust these to match your application's needs
        self.voice_name = "en-US-AriaNeural"  # Specific voice model - change to your preferred voice
        self.speech_rate = "0.9"              # Speech speed: 0.5=slow, 0.9=slightly slow, 1.0=normal, 1.2=fast
        self.pitch = "+5%"                    # Voice pitch: -50% to +50%, or low/medium/high
        self.volume = "soft"                  # Volume level: soft, medium, loud, or -50% to +50%
        
        # 💡 IMPORTANT: These exact values will be used in SSML for all calls
        # This creates a consistent, branded voice experience
        
        # Set consistent voice in config
        self.speech_config.speech_synthesis_voice_name = self.voice_name
        
        print(f"🎛️ Voice Agent initialized with custom parameters:")
        print(f"   Voice: {self.voice_name}")
        print(f"   Rate: {self.speech_rate}, Pitch: {self.pitch}, Volume: {self.volume}")
    
    def create_custom_ssml(self, text):
        """
        Create SSML with custom voice parameters for fine-tuned speech
        
        SSML = Speech Synthesis Markup Language
        XML-based markup that provides precise control over voice characteristics
        """
        ssml_template = f'''
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
            <!-- ↑ Root SSML element - defines this as speech markup, sets language to US English -->
            
            <voice name="{self.voice_name}">
                <!-- ↑ Specific voice model - locks the voice character (e.g., "en-US-AriaNeural") -->
                <!-- This ensures we always use the SAME voice, not a random one -->
                
                <prosody rate="{self.speech_rate}" pitch="{self.pitch}" volume="{self.volume}">
                    <!-- ↑ Prosody = HOW to speak (the voice characteristics) -->
                    <!-- rate="{self.speech_rate}" = Speech speed (0.5=slow, 0.9=slightly slow, 1.0=normal, 1.2=fast) -->
                    <!-- pitch="{self.pitch}" = Voice pitch (can use percentages like +5% or keywords like low/medium/high) -->
                    <!-- volume="{self.volume}" = Volume level (soft, medium, loud, or percentages) -->
                    <!-- These values let you fine-tune the voice for your specific use case -->
                    
                    {text}
                    <!-- ↑ The actual text to convert to speech -->
                    
                </prosody>
            </voice>
        </speak>
        '''
        return ssml_template
    
    def stream_to_wav(self, text, output_file="voice_response.wav"):
        """
        ✨ Generate speech with custom SSML voice characteristics
        
        This demonstrates fine-tuned voice control using SSML prosody parameters
        """
        try:
            # Configure audio output
            audio_config = AudioOutputConfig(filename=output_file)
            synthesizer = SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # 🎛️ CUSTOMIZATION: Use fine-tuned SSML for professional voice control
            # This demonstrates how to go beyond basic TTS with custom prosody
            ssml_text = self.create_custom_ssml(text)
            
            print(f"🎤 Generating voice for: {text[:50]}...")
            
            # Synthesize with locked parameters
            result = synthesizer.speak_ssml_async(ssml_text).get()
            
            if result.reason.name == "SynthesizingAudioCompleted":
                print(f"✅ Voice generated: {output_file}")
                return output_file
            else:
                print(f"❌ Voice generation failed: {result.reason}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

def test_voice_customization():
    """
    Test the SSML voice customization with different texts
    """
    print("�️ TESTING SSML VOICE CUSTOMIZATION")
    print("=" * 40)
    
    # Create custom voice agent
    agent = CustomVoiceAgent()
    
    # Test with different conversation responses
    test_texts = [
        "Hello! How can I help you today?",
        "That's a great question. Let me think about that.",
        "I understand your concern. Here's what I recommend.",
        "Perfect! I'm glad that solution worked for you."
    ]
    
    print("\n🎤 Generating test audio files...")
    
    for i, text in enumerate(test_texts, 1):
        output_file = f"test_response_{i}.wav"
        agent.stream_to_wav(text, output_file)
    
    print(f"\n🎧 Generated {len(test_texts)} audio files with custom voice characteristics")
    print("📂 Listen to test_response_*.wav files")
    print("🎛️ Notice the fine-tuned voice: slightly slower, higher pitch, softer volume")

if __name__ == "__main__":
    test_voice_customization()
