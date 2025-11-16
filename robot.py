#!/usr/bin/env python3
"""
Main Robot Brain - Talks to AI and controls hardware
"""
import ollama
import json
import time
from hardware import Hardware
from motors import Motors
from camera import Camera
from voice import Voice

class Robot:
    def __init__(self):
        print("🧠 Booting up robot brain...")
        
        # Initialize all hardware
        self.hardware = Hardware()
        self.motors = Motors()
        self.camera = Camera()
        self.voice = Voice()
        self.ai = ollama.Client()
        
        # Robot personality
        self.name = "LlamaBot"
        self.model = "tinyllama"
        
        print(f"✅ {self.name} is ready! Found: {self.hardware.summary()}")
    
    def think(self, user_input):
        """AI thinks about what to do"""
        prompt = f"""
        You are {self.name}, a physical robot with real hardware:
        {self.hardware.summary()}
        
        Human: {user_input}
        
        Respond briefly and naturally. If movement is needed, just say you'll do it.
        """
        
        try:
            response = self.ai.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Sorry, my brain glitched: {e}"
    
    def start_conversation(self):
        """Main conversation loop"""
        print(f"\n🤖 {self.name}: Hi! I'm ready to help!")
        print("💬 You can ask me to move, look around, or just chat!")
        print("❌ Type 'quit' to exit\n")
        
        while True:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("🤖 Robot: Thanks for chatting! Shutting down...")
                    break
                
                if not user_input:
                    continue
                
                # Let AI think
                print("🤖 Robot: ", end="")
                response = self.think(user_input)
                print(response)
                
                # Do physical actions if mentioned
                self.do_actions(user_input, response)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"🤖 Robot: Oops! {e}")
    
    def do_actions(self, user_input, response):
        """Perform physical actions based on conversation"""
        input_lower = user_input.lower()
        response_lower = response.lower()
        
        # Movement commands
        if any(word in input_lower for word in ['move', 'forward', 'backward', 'turn', 'left', 'right']):
            if 'forward' in input_lower:
                self.motors.move_forward(2)
            elif 'backward' in input_lower:
                self.motors.move_backward(2)
            elif 'left' in input_lower:
                self.motors.turn_left(1)
            elif 'right' in input_lower:
                self.motors.turn_right(1)
        
        # Camera commands
        if any(word in input_lower for word in ['see', 'look', 'camera', 'what do you see']):
            what_i_see = self.camera.capture()
            print(f"👀 {self.name}: I see {what_i_see}")
        
        # Voice commands
        if any(word in input_lower for word in ['speak', 'talk', 'say hello']):
            self.voice.speak(response)
