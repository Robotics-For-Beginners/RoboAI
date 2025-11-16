#!/bin/bash
echo "🤖 Installing Llama Robot..."
echo "============================"

# Install Ollama for AI brain
echo "📦 Installing AI engine..."
curl -fsSL https://ollama.ai/install.sh | sh

# Download TinyLlama (small but capable)
echo "🧠 Downloading robot brain (TinyLlama)..."
ollama pull tinyllama

# Install Python packages
echo "🐍 Installing robot dependencies..."
pip3 install gpiozero opencv-python pillow speechrecognition pyaudio

echo ""
echo "✅ Installation complete!"
echo "🚀 Run: python3 start-robot.py"
echo "💡 Make sure your Raspberry Pi is connected to motors and camera!" 
