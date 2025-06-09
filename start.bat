@echo off
title Discord Invite Bot Launcher
echo 🚀 Starting Discord Invite Bot...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing requirements...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found! Please copy .env.example to .env and configure it.
    pause
    exit /b 1
)

REM Create logs directory if it doesn't exist
if not exist "logs" (
    echo 📁 Creating logs directory...
    mkdir logs
)

REM Start the bot in background
echo 🤖 Starting bot in background mode...
echo 📝 All logs will be saved to logs/bot.log
echo.

REM Start bot and redirect all output to log file
start /MIN python main.py > logs/bot.log 2>&1

REM Wait a moment for bot to initialize
timeout /t 3 /nobreak >nul

echo ✅ Bot has been started in background!
echo 📋 Check logs/bot.log for detailed output
echo 🛑 To stop the bot, close python.exe in Task Manager
echo.
pause
