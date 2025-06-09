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

# Create logs directory if it doesn't exist
if [ ! -d "logs" ]; then
    echo "📁 Creating logs directory..."
    mkdir -p logs
fi

# Start the bot in background
echo "🤖 Starting bot in background mode..."
echo "📝 All logs will be saved to logs/bot.log"
echo ""

# Start bot in background and save PID
nohup python main.py > logs/bot.log 2>&1 &
BOT_PID=$!

# Save PID to file for reference
echo $BOT_PID > logs/bot.pid

# Wait a moment for bot to initialize
sleep 3

# Check if process is still running
if kill -0 $BOT_PID 2>/dev/null; then
    echo "✅ Bot has been started in background!"
    echo "📋 Process ID: $BOT_PID"
    echo "📝 Check logs/bot.log for detailed output"
    echo "🛑 To stop the bot, run: kill $BOT_PID"
    echo ""
    echo "📊 Recent startup logs:"
    echo "----------------------------------------"
    tail -n 5 logs/bot.log 2>/dev/null || echo "Bot is still initializing..."
else
    echo "❌ Failed to start bot! Check logs/bot.log for errors"
    cat logs/bot.log 2>/dev/null | tail -n 10
    exit 1
fi
