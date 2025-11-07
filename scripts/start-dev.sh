#!/bin/bash
# Quick start script for development

set -e

echo "🚀 Starting CrewAI Event Monitor..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Windows (Git Bash or WSL)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo -e "${YELLOW}Running on Windows${NC}"
    # Use PowerShell commands
    ACTIVATE_CMD=".\\crewai_env\\Scripts\\Activate.ps1"
else
    ACTIVATE_CMD="source crewai_env/bin/activate"
fi

echo -e "${YELLOW}Prerequisites:${NC}"
echo "1. LM Studio running on http://localhost:1234/v1"
echo "2. Python 3.11+ installed"
echo "3. Node.js 18+ installed"
echo ""

echo -e "${YELLOW}Step 1: Checking virtual environment...${NC}"
if [ ! -d "crewai_env" ]; then
    echo -e "${RED}Virtual environment not found!${NC}"
    echo "Create with: python -m venv crewai_env"
    exit 1
fi
echo -e "${GREEN}✓ Virtual environment found${NC}"
echo ""

echo -e "${YELLOW}Step 2: Setting up for development...${NC}"
echo "You need to run these commands in separate terminals:"
echo ""

echo -e "${GREEN}Terminal 1 - Backend:${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  powershell -NoExit -Command \"$ACTIVATE_CMD; cd backend; python server.py\""
else
    echo "  $ACTIVATE_CMD"
    echo "  python backend/server.py"
fi
echo ""

echo -e "${GREEN}Terminal 2 - Frontend:${NC}"
echo "  cd frontend"
echo "  npm run dev"
echo ""

echo -e "${GREEN}Terminal 3 - Run CrewAI:${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  powershell -NoExit -Command \"$ACTIVATE_CMD; python runner.py\""
else
    echo "  $ACTIVATE_CMD"
    echo "  python runner.py"
fi
echo ""

echo -e "${YELLOW}Once everything is running:${NC}"
echo "  Open http://localhost:5173 in your browser"
echo ""
