#!/usr/bin/env python3
"""
GPT-4o Real-time Text-to-Speech

This demonstrates using GPT-4o's real-time API for direct text-to-speech conversion
using the native audio synthesis capabilities.

ARCHITECTURE:
- GPT-4o Real-time API: Direct text-to-speech via WebSocket
- Native Audio Output: Built-in speech synthesis
- Real-time pipeline: Text input → GPT-4o TTS → Audio output
"""

import os
import json
import base64
import threading
import pyaudio
import websocket
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Azure credentials
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

if not AZURE_OPENAI_KEY or not AZURE_OPENAI_ENDPOINT:
    raise RuntimeError("❌ Missing AZURE_OPENAI_KEY or AZURE_OPENAI_ENDPOINT in .env file!")

# Try different deployment names if the primary one doesn't support audio output
DEPLOYMENT_FALLBACKS = [
    AZURE_OPENAI_DEPLOYMENT,  # Primary deployment from .env
    "gpt-4o-realtime",        # Common real-time deployment name
    "gpt-4o-realtime-preview", # Preview version
    "gpt-4o-2024-08-06",      # Version-specific deployment
    "gpt-4o-audio"            # Audio-specific deployment
]

current_deployment = DEPLOYMENT_FALLBACKS[0]

# Try different API versions that might work better
API_VERSIONS = [
    "2024-10-01-preview",     # Latest preview
    "2025-04-01-preview",     # Current version
    "2024-08-01-preview"      # Earlier preview
]

current_api_version = API_VERSIONS[0]
ws_url = f"{AZURE_OPENAI_ENDPOINT.replace('https', 'wss')}/openai/realtime?api-version={current_api_version}&deployment={current_deployment}"
headers = {"api-key": AZURE_OPENAI_KEY}

print(f"🔧 Attempting connection with deployment: {current_deployment}")
print(f"🔧 Using API version: {current_api_version}")
print(f"💡 Note: '{current_deployment}' deployment must support real-time audio output")

# Audio configuration (24kHz, mono, 16-bit PCM as per GPT-4o real-time API)
SAMPLE_RATE = 24000
CHANNELS = 1
FORMAT = pyaudio.paInt16
CHUNK_SIZE = 1024

# Initialize PyAudio for output
audio_interface = pyaudio.PyAudio()
output_stream = None
response_active = False  # Track if a response is in progress

class GPT4oTTSAgent:
    """
    GPT-4o native text-to-speech agent using real-time API
    """
    
    def __init__(self):
        self.ws = None
        self.tts_active = False
        
        print("🎤 GPT-4o TTS Agent initialized")
        print("🔊 Using GPT-4o native speech synthesis")

def on_open(ws):
    """Called when WebSocket connection is established"""
    print("✅ Connected to GPT-4o!")
    print("🤖 Configuring TTS session...")
    
    # Configure the session for text-to-speech
    session_config = {
        "type": "session.update",
        "session": {
            "modalities": ["text", "audio"],  # Enable both text and audio
            "instructions": "You are a helpful assistant. Respond to user messages with speech.",
            "voice": "alloy",  # GPT-4o voice: alloy, echo, fable, onyx, nova, shimmer
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",  # 16-bit PCM audio output
            "input_audio_transcription": {
                "model": "whisper-1"
            },
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.5,
                "prefix_padding_ms": 300,
                "silence_duration_ms": 500
            },
            "temperature": 0.8,
            "max_response_output_tokens": 150
        }
    }
    
    ws.send(json.dumps(session_config))
    print("\n💬 Ready for text-to-speech! Enter text to convert:")
    print("=" * 50 + "\n")

def on_message(ws, message):
    """Handle incoming messages from GPT-4o"""
    global output_stream, response_active
    
    try:
        data = json.loads(message)
        event_type = data.get("type", "")
        
        # Debug: Print all event types to see what we're getting
        print(f"🔍 Event: {event_type}")
        
        # Handle audio output from GPT-4o TTS
        if event_type == "response.audio.delta":
            audio_data = data.get("delta", "")
            if audio_data:
                # Decode base64 audio and play it
                audio_bytes = base64.b64decode(audio_data)
                if output_stream:
                    output_stream.write(audio_bytes)
                    print("🎵", end='', flush=True)  # Show audio is being processed
                else:
                    print("⚠️ No output stream available")
            else:
                print("⚠️ No audio delta data")
        
        # Handle audio transcript (this shows what was spoken)
        elif event_type == "response.audio_transcript.delta":
            transcript_delta = data.get("delta", "")
            if transcript_delta:
                print(f"🗣️ Speaking: {transcript_delta}", end='', flush=True)
        
        # Handle text response (GPT-4o may respond with text too)
        elif event_type == "response.text.delta":
            text_delta = data.get("delta", "")
            if text_delta:
                print(text_delta, end='', flush=True)
        
        # Handle text response completion
        elif event_type == "response.text.done":
            text_content = data.get("text", "")
            if text_content:
                print(f"\n🤖 GPT-4o said: {text_content}")
        
        # Handle TTS completion - check if we got any actual audio
        elif event_type == "response.audio.done":
            print("\n🔊 Speech synthesis completed!")
        
        # Handle full response completion - diagnose audio issues
        elif event_type == "response.done":
            response_active = False
            if output_stream:
                output_stream.stop_stream()
                output_stream.close()
                output_stream = None
            
            # Check if we only got transcript but no audio data
            print("\n📊 Response Analysis:")
            print("  ✅ GPT-4o generated speech transcript")
            print("  ❌ No raw audio data received (response.audio.delta events missing)")
            print(f"  💡 The '{current_deployment}' deployment may not support audio output")
            print("  🔧 Try a different deployment name like 'gpt-4o' or 'gpt-4o-realtime'")
            print("\n✅ Ready for next text input")
        
        # Handle response creation
        elif event_type == "response.created":
            print("🎤 Generating speech...")
            response_active = True
            
            # Initialize audio output stream when response starts
            if not output_stream:
                output_stream = audio_interface.open(
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    output=True,
                    frames_per_buffer=CHUNK_SIZE
                )
        
        # Handle errors
        elif event_type == "error":
            error = data.get("error", {})
            print(f"\n❌ Error: {error.get('message', 'Unknown error')}")
            error_code = error.get("code", "")
            if "deployment" in error.get("message", "").lower():
                print(f"💡 Try updating AZURE_OPENAI_DEPLOYMENT in .env to a deployment that supports real-time audio")
            response_active = False
            
    except json.JSONDecodeError:
        pass  # Ignore non-JSON messages
    except Exception as e:
        print(f"\n⚠️ Message processing error: {e}")

def on_error(ws, error):
    """Handle WebSocket errors"""
    print(f"\n❌ WebSocket error: {error}")
    
    # Check if it's a deployment issue
    if "400" in str(error) and ("model" in str(error).lower() or "deployment" in str(error).lower()):
        print(f"\n💡 DEPLOYMENT ISSUE DETECTED")
        print(f"🔧 The '{current_deployment}' deployment doesn't support real-time operations")
        print(f"\n📋 SOLUTIONS:")
        print(f"1. Create a new deployment in Azure OpenAI Studio:")
        print(f"   - Go to https://oai.azure.com/")
        print(f"   - Navigate to Deployments → Create new deployment")
        print(f"   - Model: gpt-4o (choose a version that supports realtime)")
        print(f"   - Deployment name: gpt-4o-realtime")
        print(f"   - Update your .env: AZURE_OPENAI_DEPLOYMENT=gpt-4o-realtime")
        print(f"\n2. Alternative deployment names to try:")
        for deployment in DEPLOYMENT_FALLBACKS[1:]:
            print(f"   - {deployment}")
        print(f"\n3. Check if your Azure region ({AZURE_OPENAI_ENDPOINT}) supports GPT-4o realtime")
        print(f"   - Some regions may not have realtime capabilities yet")
        
def try_next_deployment():
    """Try the next deployment in the fallback list"""
    global current_deployment, ws_url
    
    current_index = DEPLOYMENT_FALLBACKS.index(current_deployment)
    if current_index < len(DEPLOYMENT_FALLBACKS) - 1:
        current_deployment = DEPLOYMENT_FALLBACKS[current_index + 1]
        ws_url = f"{AZURE_OPENAI_ENDPOINT.replace('https', 'wss')}/openai/realtime?api-version={current_api_version}&deployment={current_deployment}"
        print(f"\n🔄 Trying next deployment: {current_deployment}")
        return True
    return False

def on_close(ws, close_status_code, close_msg):
    """Clean up when WebSocket closes"""
    global output_stream
    print("\n\n🔌 Disconnected from GPT-4o")
    
    if output_stream:
        output_stream.stop_stream()
        output_stream.close()
    audio_interface.terminate()

def send_text_for_speech(ws, text):
    """Send text to GPT-4o for speech synthesis"""
    global response_active
    
    if response_active:
        print("⏳ Please wait for current response to finish...")
        return
        
    if ws and text.strip():
        # Create conversation item with text
        message = {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": text
                    }
                ]
            }
        }
        
        ws.send(json.dumps(message))
        
        # Trigger response with both text and audio output
        response_trigger = {
            "type": "response.create",
            "response": {
                "modalities": ["text", "audio"],  # Request both text and audio output
                "instructions": f"Please speak this text naturally: {text}"
            }
        }
        ws.send(json.dumps(response_trigger))
        
        print(f"� Text: {text}")

def main():
    """Main function to run the TTS client"""
    global output_stream
    
    print("🚀 GPT-4o Real-time Text-to-Speech Demo")
    print("=" * 50)
    
    # List available audio output devices
    print("\n📋 Available audio output devices:")
    for i in range(audio_interface.get_device_count()):
        info = audio_interface.get_device_info_by_index(i)
        if info["maxOutputChannels"] > 0:
            print(f"  [{i}] {info['name']}")
    
    print(f"\n🔗 Connecting to: {AZURE_OPENAI_ENDPOINT}")
    print(f"🎯 Using deployment: {current_deployment}")
    print("🎤 GPT-4o native text-to-speech")
    print("💡 NOTE: Deployment must support real-time audio output (not just transcription)")
    print("=" * 50 + "\n")
    
    # Create and run WebSocket connection
    ws_app = websocket.WebSocketApp(
        ws_url,
        header=headers,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    # Start WebSocket in background thread
    def run_ws():
        ws_app.run_forever()
    
    ws_thread = threading.Thread(target=run_ws, daemon=True)
    ws_thread.start()
    
    # Wait for connection
    import time
    time.sleep(2)
    
    # Main TTS loop
    try:
        while True:
            text_input = input("\nEnter text to speak (or 'quit' to exit): ")
            
            if text_input.lower() in ['quit', 'exit', 'bye']:
                break
            
            if text_input.strip():
                send_text_for_speech(ws_app, text_input)
                
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopping TTS...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        if output_stream:
            output_stream.stop_stream()
            output_stream.close()
        audio_interface.terminate()

if __name__ == "__main__":
    main()
