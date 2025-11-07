@echo off
REM Quick start script for Windows PowerShell

echo.
echo ========================================
echo   CrewAI Event Monitor - Setup Helper
echo ========================================
echo.
echo This script will help you start the development environment.
echo.
echo Prerequisites:
echo   1. LM Studio running on http://localhost:1234/v1
echo   2. Python 3.11+
echo   3. Node.js 18+
echo.
echo Instructions:
echo.
echo Step 1: Start Backend Server
echo   Open a PowerShell window in this folder and run:
echo   .\crewai_env\Scripts\Activate.ps1
echo   python backend\server.py
echo.
echo Step 2: Start Frontend Dev Server  
echo   Open another PowerShell window in this folder and run:
echo   cd frontend
echo   npm run dev
echo.
echo Step 3: Run CrewAI Crew
echo   Open a third PowerShell window in this folder and run:
echo   .\crewai_env\Scripts\Activate.ps1
echo   python runner.py
echo.
echo Step 4: View the Dashboard
echo   Open http://localhost:5173 in your browser
echo.
pause
