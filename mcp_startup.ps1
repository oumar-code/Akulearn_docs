# MCP Server Startup Script (PowerShell)
# Initializes all configured MCP servers

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 MCP INFRASTRUCTURE STARTUP" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if .env file exists
if (Test-Path ".env") {
    Write-Host "📂 Loading environment variables from .env..." -ForegroundColor Green
    Get-Content .env | Where-Object { $_ -notmatch '^\s*#' -and $_ -match '=' } | ForEach-Object {
        $name, $value = $_ -split '=', 2
        [Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), "Process")
    }
    Write-Host "✅ Environment variables loaded`n" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found. Using system environment variables.`n" -ForegroundColor Yellow
}

# Function to check if a command exists
function Test-CommandExists {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

$missing = @()

if (-not (Test-CommandExists "node")) {
    $missing += "Node.js"
}
if (-not (Test-CommandExists "npm")) {
    $missing += "npm"
}
if (-not (Test-CommandExists "python")) {
    $missing += "Python"
}
if (-not (Test-CommandExists "git")) {
    $missing += "Git"
}

if ($missing.Count -gt 0) {
    Write-Host "❌ Missing prerequisites:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    exit 1
} else {
    Write-Host "✅ All prerequisites available`n" -ForegroundColor Green
}

# Run MCP initialization script
Write-Host "🔧 Running MCP initialization..." -ForegroundColor Yellow

try {
    python mcp_init.py
} catch {
    Write-Host "❌ MCP initialization failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ MCP Infrastructure ready!" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor Green
Write-Host "  1. Update .env with your API keys" -ForegroundColor Green
Write-Host "  2. Run: python mcp_server.py" -ForegroundColor Green
Write-Host "  3. Use content generation scripts`n" -ForegroundColor Green

# Optional: Start MCP servers automatically
$startServers = Read-Host "Start MCP servers now? (y/n)"
if ($startServers -eq "y") {
    python mcp_server.py
}
