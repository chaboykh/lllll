@echo off
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


REM Start the bot
echo 🤖 Starting bot...
python main.py
pause
