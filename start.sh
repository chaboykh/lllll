#!/bin/bash

echo "🚀 Starting Discord Invite Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found! Please copy .env.example to .env and configure it."
    exit 1
fi

# Start the bot
echo "🤖 Starting bot..."
python main.py
