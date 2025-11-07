#!/usr/bin/env node

/**
 * Setup script for CrewAI Event Monitor frontend and backend
 * Run: node setup.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function checkDirectory(dir) {
  return fs.existsSync(dir);
}

function runCommand(cmd, cwd = process.cwd()) {
  try {
    execSync(cmd, { cwd, stdio: 'inherit' });
    return true;
  } catch (error) {
    log(`Error running command: ${cmd}`, 'red');
    return false;
  }
}

async function setup() {
  log('\n🚀 CrewAI Event Monitor Setup', 'blue');
  log('=====================================\n', 'blue');

  const rootDir = process.cwd();

  // Check structure
  log('📁 Checking directory structure...', 'yellow');
  const dirs = ['backend', 'frontend', 'core', 'outputs'];
  let allExist = true;
  
  for (const dir of dirs) {
    const exists = checkDirectory(path.join(rootDir, dir));
    log(`  ${exists ? '✓' : '✗'} ${dir}/`, exists ? 'green' : 'red');
    if (!exists && dir !== 'outputs') allExist = false;
  }

  if (!allExist) {
    log('\n⚠️  Some required directories are missing!', 'red');
    return;
  }

  // Check Python
  log('\n🐍 Checking Python installation...', 'yellow');
  try {
    const pythonVersion = execSync('python --version', { encoding: 'utf-8' }).trim();
    log(`  ✓ ${pythonVersion}`, 'green');
  } catch {
    log('  ✗ Python not found or not in PATH', 'red');
    return;
  }

  // Check Node.js
  log('\n📦 Checking Node.js installation...', 'yellow');
  try {
    const nodeVersion = execSync('node --version', { encoding: 'utf-8' }).trim();
    log(`  ✓ Node.js ${nodeVersion}`, 'green');
  } catch {
    log('  ✗ Node.js not found or not in PATH', 'red');
    return;
  }

  // Create .env if doesn't exist
  log('\n⚙️  Setting up environment...', 'yellow');
  const envPath = path.join(rootDir, '.env');
  const envExamplePath = path.join(rootDir, '.env.example');
  
  if (!fs.existsSync(envPath) && fs.existsSync(envExamplePath)) {
    fs.copyFileSync(envExamplePath, envPath);
    log('  ✓ Created .env from .env.example', 'green');
  } else if (fs.existsSync(envPath)) {
    log('  ✓ .env already exists', 'green');
  }

  // Setup frontend
  log('\n📝 Setting up frontend...', 'yellow');
  const frontendDir = path.join(rootDir, 'frontend');
  
  if (!fs.existsSync(path.join(frontendDir, 'node_modules'))) {
    log('  Installing dependencies...', 'yellow');
    if (!runCommand('npm install', frontendDir)) {
      log('  ✗ Failed to install frontend dependencies', 'red');
    } else {
      log('  ✓ Frontend dependencies installed', 'green');
    }
  } else {
    log('  ✓ node_modules already exists', 'green');
  }

  // Setup backend (optional - only if venv doesn't exist)
  log('\n🐍 Backend setup info:', 'yellow');
  const backendDir = path.join(rootDir, 'backend');
  const venvPath = path.join(rootDir, 'crewai_env');
  
  if (fs.existsSync(venvPath)) {
    log('  ✓ Virtual environment found at ./crewai_env', 'green');
    log('  To activate: .\\crewai_env\\Scripts\\Activate.ps1', 'blue');
  } else {
    log('  ℹ Virtual environment not found', 'yellow');
    log('  Create with: python -m venv crewai_env', 'blue');
    log('  Activate with: .\\crewai_env\\Scripts\\Activate.ps1', 'blue');
    log('  Install deps with: pip install -r backend\\requirements.txt', 'blue');
  }

  // Create outputs directory if needed
  const outputsDir = path.join(rootDir, 'outputs');
  if (!fs.existsSync(outputsDir)) {
    fs.mkdirSync(outputsDir, { recursive: true });
    log('\n  ✓ Created outputs directory', 'green');
  }

  // Summary
  log('\n✅ Setup Complete!', 'green');
  log('\n📋 Next steps:', 'blue');
  log('\n1. Ensure LM Studio is running on http://localhost:1234/v1', 'yellow');
  log('\n2. Start the backend server:', 'yellow');
  log('   .\\crewai_env\\Scripts\\Activate.ps1', 'blue');
  log('   python backend\\server.py', 'blue');
  log('\n3. Start the frontend dev server (new terminal):', 'yellow');
  log('   cd frontend', 'blue');
  log('   npm run dev', 'blue');
  log('\n4. Run your CrewAI crew (new terminal):', 'yellow');
  log('   .\\crewai_env\\Scripts\\Activate.ps1', 'blue');
  log('   python runner.py', 'blue');
  log('\n5. Open http://localhost:5173 in your browser', 'yellow');
  log('\n📚 For detailed setup, see FRONTEND_SETUP.md', 'blue');
  log('\n');
}

setup().catch(error => {
  log(`\n❌ Setup failed: ${error.message}`, 'red');
  process.exit(1);
});
