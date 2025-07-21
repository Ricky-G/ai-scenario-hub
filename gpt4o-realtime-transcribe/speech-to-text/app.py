#!/usr/bin/env python3
"""
Simple Azure OpenAI GPT-4o Transcribe Real-time Speech-to-Text Script

This script connects to Azure OpenAI's transcription-specific endpoint
and streams microphone audio for real-time transcription.
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

if not AZURE_OPENAI_KEY or not AZURE_OPENAI_ENDPOINT:
    raise RuntimeError("❌ Missing AZURE_OPENAI_KEY or AZURE_OPENAI_ENDPOINT in .env file!")

# Convert HTTPS endpoint to WSS and add transcription intent
# Example: https://myresource.openai.azure.com/ -> wss://myresource.openai.azure.com/
ws_url = f"{AZURE_OPENAI_ENDPOINT.replace('https', 'wss')}/openai/realtime?api-version=2025-04-01-preview&intent=transcription"
headers = {"api-key": AZURE_OPENAI_KEY}

# Audio configuration (24kHz, mono, 16-bit PCM as per the blog)
SAMPLE_RATE = 24000
CHANNELS = 1
FORMAT = pyaudio.paInt16
CHUNK_SIZE = 1024

# Initialize PyAudio
audio_interface = pyaudio.PyAudio()
stream = None

def on_open(ws):
    """Called when WebSocket connection is established"""
    print("✅ Connected! Configuring session...")
    
    # Configure the transcription session
    session_config = {
        "type": "transcription_session.update",
        "session": {
            "input_audio_format": "pcm16",
            "input_audio_transcription": {
                "model": "gpt-4o-transcribe",  # Changed from gpt-4o-mini-transcribe
                "prompt": "Transcribe the audio accurately.",
                "language": "en"  # Set to specific language code like "en" if needed
            },
            "input_audio_noise_reduction": {
                "type": "near_field"  # Use "far_field" for conference rooms
            },
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.5,
                "prefix_padding_ms": 300,
                "silence_duration_ms": 200
            }
        }
    }
    
    ws.send(json.dumps(session_config))
    print("🎤 Start speaking... (Press Ctrl+C to stop)\n")
    
    # Start streaming microphone audio in a separate thread
    def stream_microphone():
        try:
            while ws.keep_running:
                # Read audio chunk from microphone
                audio_data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                
                # Convert to base64 and send
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                ws.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "audio": audio_base64
                }))
        except Exception as e:
            print(f"❌ Audio streaming error: {e}")
            ws.close()
    
    threading.Thread(target=stream_microphone, daemon=True).start()

def on_message(ws, message):
    """Handle incoming messages from the WebSocket"""
    try:
        data = json.loads(message)
        event_type = data.get("type", "")
        
        # Handle incremental transcription updates (partial results)
        if event_type == "conversation.item.input_audio_transcription.delta":
            transcript_piece = data.get("delta", "")
            if transcript_piece:
                print(transcript_piece, end='', flush=True)
        
        # Handle completed transcription segments
        elif event_type == "conversation.item.input_audio_transcription.completed":
            transcript = data.get("transcript", "")
            if transcript:
                print(f"\n📝 Completed: {transcript}\n")
        
        # Handle any error events
        elif event_type == "error":
            error = data.get("error", {})
            print(f"\n❌ Error: {error.get('message', 'Unknown error')}")
            
    except json.JSONDecodeError:
        pass  # Ignore non-JSON messages
    except Exception as e:
        print(f"\n⚠️ Message processing error: {e}")

def on_error(ws, error):
    """Handle WebSocket errors"""
    print(f"\n❌ WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Clean up when WebSocket closes"""
    print("\n\n🔌 Disconnected from server")
    if stream:
        stream.stop_stream()
        stream.close()
    audio_interface.terminate()

def main():
    """Main function to run the transcription client"""
    global stream
    
    print("🚀 Azure OpenAI GPT-4o Transcribe Demo")
    print("=" * 50)
    
    # List available audio input devices
    print("\n📋 Available audio input devices:")
    for i in range(audio_interface.get_device_count()):
        info = audio_interface.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"  [{i}] {info['name']}")
    
    # Open microphone stream
    try:
        stream = audio_interface.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE
        )
    except Exception as e:
        print(f"\n❌ Failed to open microphone: {e}")
        print("Please check your audio settings and try again.")
        return
    
    print(f"\n🔗 Connecting to: {AZURE_OPENAI_ENDPOINT}")
    print("📡 Using transcription intent with GPT-4o-transcribe")
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
    
    try:
        ws_app.run_forever()
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopping transcription...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        if stream:
            stream.stop_stream()
            stream.close()
        audio_interface.terminate()

if __name__ == "__main__":
    main()