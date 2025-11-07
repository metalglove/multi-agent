# Docker + Runner Startup Script for Windows (PowerShell)
# Usage: .\scripts\start-docker-dev.ps1

param(
    [switch]$Docker = $false,
    [switch]$Runner = $false,
    [switch]$Bridge = $false,
    [switch]$All = $false
)

# Show help
if (-not $Docker -and -not $Runner -and -not $Bridge -and -not $All) {
    Write-Host "CrewAI Docker + Runner Startup Script" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\scripts\start-docker-dev.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Green
    Write-Host "  -Docker    Start Docker services (Redis, Bridge, Frontend)"
    Write-Host "  -Runner    Start runner in new window"
    Write-Host "  -Bridge    Start bridge in new window (for local development)"
    Write-Host "  -All       Start everything"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  # Start Docker services only"
    Write-Host "  .\scripts\start-docker-dev.ps1 -Docker"
    Write-Host ""
    Write-Host "  # Start Docker and runner"
    Write-Host "  .\scripts\start-docker-dev.ps1 -Docker -Runner"
    Write-Host ""
    Write-Host "  # Start everything"
    Write-Host "  .\scripts\start-docker-dev.ps1 -All"
    Write-Host ""
    exit
}

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $ProjectRoot

# Load .env if it exists
$EnvFile = Join-Path $ProjectRoot ".env"
if (Test-Path $EnvFile) {
    Write-Host "Loading .env file..." -ForegroundColor Gray
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -and -not $_.StartsWith("#")) {
            $name, $value = $_.Split("=", 2)
            if ($name -and $value) {
                [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), "Process")
            }
        }
    }
}

# Ensure REDIS_URL is set
if (-not $env:REDIS_URL) {
    $env:REDIS_URL = "redis://127.0.0.1:6379/0"
}
if (-not $env:REDIS_CHANNEL) {
    $env:REDIS_CHANNEL = "crewai:events"
}

Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  REDIS_URL: $env:REDIS_URL"
Write-Host "  REDIS_CHANNEL: $env:REDIS_CHANNEL"
Write-Host ""

# Start Docker services
if ($Docker -or $All) {
    Write-Host "Starting Docker services..." -ForegroundColor Green
    docker-compose up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Docker services started" -ForegroundColor Green
        Write-Host "  - Redis: redis://127.0.0.1:6379"
        Write-Host "  - Bridge: http://localhost:8000"
        Write-Host "  - Frontend: http://localhost:5173"
        Write-Host ""
    } else {
        Write-Host "✗ Failed to start Docker services" -ForegroundColor Red
        exit 1
    }
}

# Start runner in new window
if ($Runner -or $All) {
    Write-Host "Starting runner in new window..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "
        Set-Location '$ProjectRoot'
        `$env:REDIS_URL = '$env:REDIS_URL'
        `$env:REDIS_CHANNEL = '$env:REDIS_CHANNEL'
        Write-Host 'Runner - REDIS_URL: `$env:REDIS_URL' -ForegroundColor Cyan
        python -m src.backend.runner_with_monitoring
    " -WindowStyle Normal
    Write-Host "✓ Runner started in new window" -ForegroundColor Green
}

# Start bridge in new window (for local development)
if ($Bridge) {
    Write-Host "Starting bridge in new window..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "
        Set-Location '$ProjectRoot'
        `$env:REDIS_URL = 'redis://127.0.0.1:6379/0'
        `$env:REDIS_CHANNEL = 'crewai:events'
        `$env:BRIDGE_PORT = '8000'
        Write-Host 'Bridge - REDIS_URL: `$env:REDIS_URL' -ForegroundColor Cyan
        uvicorn src.bridge.app:app --host 127.0.0.1 --port 8000 --reload
    " -WindowStyle Normal
    Write-Host "✓ Bridge started in new window" -ForegroundColor Green
}

Write-Host ""
Write-Host "Services are starting..." -ForegroundColor Cyan
Write-Host ""

# Show next steps
if ($Docker -or $All) {
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Wait for services to be healthy (check 'docker-compose ps')"
    Write-Host "  2. Open http://localhost:5173 in your browser"
    Write-Host "  3. Runner will start publishing events to Redis"
    Write-Host ""
    Write-Host "To view logs:" -ForegroundColor Yellow
    Write-Host "  docker-compose logs -f bridge"
    Write-Host ""
    Write-Host "To stop services:" -ForegroundColor Yellow
    Write-Host "  docker-compose down"
}
