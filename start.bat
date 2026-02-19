@echo off
REM Windows startup script for PharmaGuard

echo Starting PharmaGuard...

REM Start backend
start "PharmaGuard Backend" cmd /k "cd backend && python app.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
start "PharmaGuard Frontend" cmd /k "npm run dev"

echo Both servers starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
