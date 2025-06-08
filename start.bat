@echo off
title Discord Invite Bot
echo 🚀 Starting Discord Invite Bot...

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found! Please copy .env.example to .env and configure it.
    pause
    exit /b 1
)

REM Check if logs directory exists
if not exist "logs" (
    echo 📁 Creating logs directory...
    mkdir logs
)

echo 🤖 Starting bot in console mode...
echo 📝 Logs will be saved to logs/bot.log
echo 🔄 Bot will run in background after startup...
echo.

REM Start bot and redirect output to log file while showing in console initially
node index.js 2>&1 | tee logs/bot.log

pause
