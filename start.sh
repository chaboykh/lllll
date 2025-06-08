#!/bin/bash

echo "🚀 Starting Discord Invite Bot..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found! Please copy .env.example to .env and configure it."
    exit 1
fi

# Check if logs directory exists
if [ ! -d "logs" ]; then
    echo "📁 Creating logs directory..."
    mkdir -p logs
fi

echo "🤖 Starting bot in console mode..."
echo "📝 Logs will be saved to logs/bot.log"
echo "🔄 Bot will run in background after startup..."
echo ""

# Function to handle cleanup
cleanup() {
    echo ""
    echo "🛑 Stopping bot..."
    kill $BOT_PID 2>/dev/null
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Start bot in background and save PID
node index.js > logs/bot.log 2>&1 &
BOT_PID=$!

# Show initial logs in console for 10 seconds
echo "📋 Showing startup logs (10 seconds)..."
timeout 10s tail -f logs/bot.log || gtimeout 10s tail -f logs/bot.log 2>/dev/null || {
    # Fallback for systems without timeout
    tail -f logs/bot.log &
    TAIL_PID=$!
    sleep 10
    kill $TAIL_PID 2>/dev/null
}

echo ""
echo "✅ Bot is now running in background!"
echo "📝 Check logs/bot.log for full output"
echo "🛑 Press Ctrl+C to stop the bot"
echo ""

# Wait for bot process
wait $BOT_PID
