#!/bin/bash
# Installation Helper for Windows PowerShell

$ErrorActionPreference = "Stop"

Write-Host "🚀 CrewAI Event Monitor - Installation Helper`n" -ForegroundColor Cyan

# Function to check if command exists
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    }
    catch {
        return $false
    }
}

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
}
else {
    Write-Host "✗ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
if (Test-Command node) {
    $nodeVersion = node --version
    Write-Host "✓ Node.js $nodeVersion" -ForegroundColor Green
}
else {
    Write-Host "✗ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check directories
Write-Host "`nChecking directories..." -ForegroundColor Yellow
$dirs = @("backend", "frontend", "core")
foreach ($dir in $dirs) {
    if (Test-Path $dir) {
        Write-Host "✓ $dir/" -ForegroundColor Green
    }
    else {
        Write-Host "✗ $dir/ not found" -ForegroundColor Red
    }
}

# Frontend setup
Write-Host "`nSetting up frontend..." -ForegroundColor Yellow
if (-not (Test-Path "frontend/node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    Push-Location frontend
    npm install
    Pop-Location
    Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
}
else {
    Write-Host "✓ Frontend dependencies already installed" -ForegroundColor Green
}

# Create .env if needed
if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Copy-Item ".env.example" ".env"
    Write-Host "`n✓ Created .env from .env.example" -ForegroundColor Green
}

# Summary
Write-Host "`n✅ Installation Complete!" -ForegroundColor Green
Write-Host "`n📚 Next Steps:" -ForegroundColor Cyan
Write-Host "
1. Ensure LM Studio is running on http://localhost:1234/v1

2. Start Backend Server:
   .\crewai_env\Scripts\Activate.ps1
   python backend\server.py

3. Start Frontend Dev Server (new terminal):
   cd frontend
   npm run dev

4. Run CrewAI Crew (new terminal):
   .\crewai_env\Scripts\Activate.ps1
   python runner.py

5. Open Dashboard:
   http://localhost:5173

📖 Documentation:
   - FRONTEND_SETUP.md     - Complete setup guide
   - INTEGRATION_GUIDE.md  - Integration instructions
   - QUICK_REFERENCE.md    - Command reference
" -ForegroundColor Blue
