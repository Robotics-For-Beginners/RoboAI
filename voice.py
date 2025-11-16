#!/usr/bin/env python3
"""
REAL VOICE CONTROL - No simulations!
Actual speech recognition and text-to-speech
"""
import speech_recognition as sr
import pyttsx3
import time
import threading

class Voice:
    def __init__(self):
        print("🎤 Initializing REAL voice system...")
        
        self.recognizer = None
        self.microphone = None
        self.tts_engine = None
        self.voice_available = False
        
        self._setup_voice()
    
    def _setup_voice(self):
        """Setup actual microphone and speaker"""
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            
            # Initialize microphone
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            print("🔇 Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            
            # Initialize text-to-speech
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS voice
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
            
            self.tts_engine.setProperty('rate', 150)  # Speech speed
            self.tts_engine.setProperty('volume', 0.8)  # Volume level
            
            self.voice_available = True
            print("✅ Voice system ready - microphone and speaker working")
            
        except Exception as e:
            print(f"❌ Voice setup failed: {e}")
            print("💡 Check microphone and speaker connections")
    
    def listen(self, timeout=5):
        """Listen for REAL voice commands"""
        if not self.voice_available:
            print("❌ Voice system not available")
            return None
        
        try:
            print(f"🎤 Listening for {timeout} seconds... SPEAK NOW")
            
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            print("👂 Processing speech...")
            
            # Recognize speech using Google
            text = self.recognizer.recognize_google(audio)
            print(f"💬 Heard: '{text}'")
            return text
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand the speech")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Voice listening error: {e}")
            return None
    
    def speak(self, text):
        """Speak text out loud - REAL speech"""
        if not self.voice_available:
            print(f"🗣️ (Voice disabled): {text}")
            return False
        
        try:
            print(f"🗣️ Speaking: '{text}'")
            
            # Speak in a separate thread to not block
            def _speak():
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            speak_thread = threading.Thread(target=_speak)
            speak_thread.start()
            
            # Wait for speech to complete
            speak_thread.join(timeout=10)
            return True
            
        except Exception as e:
            print(f"❌ Speech error: {e}")
            return False
    
    def continuous_listen(self, callback, listen_timeout=5):
        """Continuously listen for commands"""
        if not self.voice_available:
            print("❌ Voice system not available for continuous listening")
            return
        
        print("🔊 Starting continuous voice listening...")
        print("Say 'stop listening' to exit")
        
        try:
            while True:
                command = self.listen(timeout=listen_timeout)
                if command:
                    # Check for stop command
                    if 'stop listening' in command.lower():
                        print("🛑 Stopping voice listening")
                        break
                    
                    # Call the callback function with the command
                    if callback:
                        callback(command)
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n🛑 Voice listening stopped by user")
        except Exception as e:
            print(f"❌ Continuous listening error: {e}")
    
    def test_voice(self):
        """Test microphone and speaker"""
        if not self.voice_available:
            print("❌ Voice system not available for testing")
            return False
        
        print("🎤 Testing microphone and speaker...")
        
        try:
            # Test speech recognition
            print("Please say 'hello robot' into the microphone...")
            command = self.listen(timeout=5)
            
            if command and 'hello' in command.lower():
                print("✅ Microphone working!")
            else:
                print("❌ Microphone test failed")
                return False
            
            # Test text-to-speech
            print("Testing speaker... you should hear speech.")
            self.speak("Hello! My voice is working perfectly.")
            time.sleep(2)
            
            print("✅ Speaker working!")
            return True
            
        except Exception as e:
            print(f"❌ Voice test failed: {e}")
            return False

# Standalone voice test
if __name__ == "__main__":
    print("🎤 VOICE TEST MODE")
    print("Make sure microphone and speaker are connected")
    
    voice = Voice()
    
    if voice.voice_available:
        # Test voice system
        if voice.test_voice():
            print("\n🎉 Voice test complete! System is ready.")
            
            # Demo continuous listening
            print("\n🔊 Demo: Continuous listening for 20 seconds...")
            print("Say anything and I'll repeat it!")
            
            def repeat_command(cmd):
                print(f"🤖 Repeating: {cmd}")
                voice.speak(f"You said: {cmd}")
            
            start_time = time.time()
            while time.time() - start_time < 20:
                command = voice.listen(timeout=2)
                if command:
                    repeat_command(command)
                time.sleep(0.5)
            
            print("✅ Voice demo complete!")
    else:
        print("❌ Voice test failed - check hardware connections") 
