#!/usr/bin/env python3
"""
Llama Robot - Main Starter
Just run this to start your robot!
"""
from robot import Robot
import time

print("🚀 Starting Llama Robot...")
print("=" * 40)

# Create robot instance
bot = Robot()

try:
    # Start the robot
    bot.start_conversation()
except KeyboardInterrupt:
    print("\n🤖 Robot: Goodbye! Shutting down...")
except Exception as e:
    print(f"🤖 Robot: Oops! {e}")
    print("💡 Check your hardware connections and try again!") 
