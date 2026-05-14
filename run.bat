@echo off
echo Starting Drive Legal...

:: Start Flask backend
echo Starting Flask backend on port 5000...
start cmd /k "cd backend && python app.py"

:: Start Chatbot server
echo Starting DriveBot on port 8000...
start cmd /k "python run_chatbot.py"

echo.
echo Flask running on http://127.0.0.1:5000
echo DriveBot running on http://127.0.0.1:8000
echo.
pause