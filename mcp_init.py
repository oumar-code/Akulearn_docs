#!/usr/bin/env python3
"""
MCP Infrastructure Initialization Script
Sets up all Model Context Protocol servers for Akulearn content generation
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPManager:
    """Manages MCP server lifecycle and configuration"""
    
    def __init__(self, config_path: str = "mcp_config.json"):
        """Initialize MCP Manager with configuration file"""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.active_servers: Dict[str, bool] = {}
        self.env_vars = self._load_environment()
        
    def _load_config(self) -> Dict:
        """Load MCP configuration from JSON file"""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            return {}
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        logger.info(f"✅ Loaded MCP config from {self.config_path}")
        return config
    
    def _load_environment(self) -> Dict[str, str]:
        """Load environment variables from .env file"""
        env = dict(os.environ)
        
        if Path(".env").exists():
            with open(".env", 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            env[key.strip()] = value.strip()
            logger.info("✅ Loaded environment variables from .env")
        
        return env
    
    def _expand_variables(self, value: str) -> str:
        """Expand environment variables in configuration values"""
        if isinstance(value, str):
            # Replace ${VAR_NAME} with environment variable values
            import re
            pattern = r'\$\{([^}]+)\}'
            
            def replacer(match):
                var_name = match.group(1)
                if var_name == "HOME":
                    return str(Path.home())
                return self.env_vars.get(var_name, match.group(0))
            
            return re.sub(pattern, replacer, value)
        return value
    
    def validate_configuration(self) -> bool:
        """Validate MCP configuration"""
        if not self.config:
            logger.error("❌ No MCP configuration loaded")
            return False
        
        required_keys = ["mcpServers", "globalSettings"]
        for key in required_keys:
            if key not in self.config:
                logger.error(f"❌ Missing required config key: {key}")
                return False
        
        logger.info("✅ Configuration validation passed")
        return True
    
    def check_prerequisites(self) -> bool:
        """Check if all MCP server prerequisites are installed"""
        logger.info("\n📋 Checking MCP server prerequisites...")
        
        missing_tools = []
        
        # Check Node.js (for npm/npx)
        try:
            subprocess.run(["node", "--version"], capture_output=True, check=True)
            logger.info("✅ Node.js is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append("Node.js (required for npm/npx)")
        
        # Check npm
        try:
            subprocess.run(["npm", "--version"], capture_output=True, check=True)
            logger.info("✅ npm is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append("npm")
        
        # Check Python
        try:
            subprocess.run([sys.executable, "--version"], capture_output=True, check=True)
            logger.info(f"✅ Python is installed ({sys.executable})")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append("Python")
        
        if missing_tools:
            logger.warning(f"\n⚠️  Missing prerequisites:")
            for tool in missing_tools:
                logger.warning(f"   - {tool}")
            return False
        
        logger.info("✅ All prerequisites present\n")
        return True
    
    def install_mcp_servers(self) -> bool:
        """Install MCP server packages"""
        logger.info("\n📦 Installing MCP server packages...")
        
        servers = self.config.get("mcpServers", {})
        npm_packages = set()
        
        # Collect npm packages to install
        for server_name, server_config in servers.items():
            if not server_config.get("enabled", False):
                continue
            
            args = server_config.get("args", [])
            for arg in args:
                if arg.startswith("@modelcontextprotocol"):
                    npm_packages.add(arg)
        
        if npm_packages:
            for package in npm_packages:
                try:
                    logger.info(f"Installing {package}...")
                    subprocess.run(
                        ["npm", "install", "-g", package],
                        check=True,
                        capture_output=True
                    )
                    logger.info(f"✅ Installed {package}")
                except subprocess.CalledProcessError as e:
                    logger.error(f"❌ Failed to install {package}: {e}")
                    return False
        
        logger.info("✅ MCP server packages installed\n")
        return True
    
    def test_server_connection(self, server_name: str) -> bool:
        """Test connection to a specific MCP server"""
        server_config = self.config["mcpServers"].get(server_name, {})
        
        if not server_config.get("enabled"):
            logger.info(f"⏭️  {server_name} is disabled, skipping test")
            return True
        
        logger.info(f"Testing connection to {server_name}...")
        
        try:
            command = server_config.get("command")
            args = server_config.get("args", [])
            
            # For npm packages, test if they're callable
            if command == "npx":
                test_args = args + ["--help"]
                result = subprocess.run(
                    [command] + test_args,
                    capture_output=True,
                    timeout=10
                )
                if result.returncode == 0:
                    logger.info(f"✅ {server_name} connection successful")
                    self.active_servers[server_name] = True
                    return True
            
            logger.warning(f"⚠️  Could not fully test {server_name}")
            return False
            
        except subprocess.TimeoutExpired:
            logger.error(f"❌ {server_name} connection timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Error testing {server_name}: {e}")
            return False
    
    def generate_startup_script(self, output_path: str = "mcp_startup.sh") -> bool:
        """Generate startup script for all MCP servers"""
        logger.info(f"\n📝 Generating startup script: {output_path}")
        
        script_content = """#!/bin/bash
# Auto-generated MCP Server Startup Script
# Generated: 2026-01-04

set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

echo "${GREEN}🚀 Starting MCP Servers...${NC}"

# Load environment variables
if [ -f .env ]; then
    set -a
    source .env
    set +a
    echo "${GREEN}✅ Loaded environment variables${NC}"
fi

# Function to start MCP server
start_server() {
    local server_name=$1
    local command=$2
    shift 2
    local args="$@"
    
    echo "${YELLOW}Starting $server_name...${NC}"
    eval "$command $args &"
    sleep 2
    echo "${GREEN}✅ $server_name started${NC}"
}

# Start enabled servers
"""
        
        for server_name, server_config in self.config.get("mcpServers", {}).items():
            if server_config.get("enabled"):
                command = server_config.get("command")
                args = " ".join(server_config.get("args", []))
                script_content += f'\nstart_server "{server_name}" "{command}" {args}'
        
        script_content += """

echo "${GREEN}
✅ All MCP servers started successfully!
${NC}"

# Keep process running
wait
"""
        
        with open(output_path, 'w') as f:
            f.write(script_content)
        
        # Make script executable on Unix-like systems
        if os.name != 'nt':
            os.chmod(output_path, 0o755)
        
        logger.info(f"✅ Startup script generated: {output_path}")
        return True
    
    def generate_windows_startup_script(self, output_path: str = "mcp_startup.ps1") -> bool:
        """Generate PowerShell startup script for Windows"""
        logger.info(f"\n📝 Generating Windows startup script: {output_path}")
        
        script_content = """# Auto-generated MCP Server Startup Script (PowerShell)
# Generated: 2026-01-04

function Start-MCPServers {
    Write-Host "🚀 Starting MCP Servers..." -ForegroundColor Green
    
    # Load environment variables from .env
    if (Test-Path ".env") {
        Get-Content .env | Where-Object { $_ -notmatch '^\s*#' -and $_ -match '=' } | ForEach-Object {
            $name, $value = $_ -split '=', 2
            [Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim())
        }
        Write-Host "✅ Loaded environment variables" -ForegroundColor Green
    }
    
    # Start servers
"""
        
        for server_name, server_config in self.config.get("mcpServers", {}).items():
            if server_config.get("enabled"):
                command = server_config.get("command")
                args = " " + " ".join(server_config.get("args", []))
                script_content += f'''
    Write-Host "Starting {server_name}..." -ForegroundColor Yellow
    Start-Process -NoNewWindow -FilePath "{command}" -ArgumentList "{args}" -PassThru | Out-Null
    Start-Sleep -Seconds 2
    Write-Host "✅ {server_name} started" -ForegroundColor Green
'''
        
        script_content += """
    Write-Host "
✅ All MCP servers started successfully!" -ForegroundColor Green
}

# Run the function
Start-MCPServers
"""
        
        with open(output_path, 'w') as f:
            f.write(script_content)
        
        logger.info(f"✅ Windows startup script generated: {output_path}")
        return True
    
    def print_summary(self):
        """Print configuration summary"""
        logger.info("\n" + "="*60)
        logger.info("📊 MCP CONFIGURATION SUMMARY")
        logger.info("="*60)
        
        logger.info("\n🔧 Enabled Servers:")
        for server_name, server_config in self.config.get("mcpServers", {}).items():
            if server_config.get("enabled"):
                status = "✅" if self.active_servers.get(server_name, False) else "⏳"
                logger.info(f"  {status} {server_name}: {server_config.get('description', 'No description')}")
        
        logger.info("\n⚙️  Global Settings:")
        for key, value in self.config.get("globalSettings", {}).items():
            logger.info(f"  - {key}: {value}")
        
        logger.info("\n🔗 Integrations:")
        for integration_name, integration_config in self.config.get("integrations", {}).items():
            servers = ", ".join(integration_config.get("mcpServers", []))
            logger.info(f"  - {integration_name}: {servers}")
        
        logger.info("\n" + "="*60 + "\n")


def main():
    """Main setup function"""
    logger.info("\n" + "="*60)
    logger.info("🔧 MCP INFRASTRUCTURE SETUP")
    logger.info("="*60 + "\n")
    
    # Initialize manager
    manager = MCPManager()
    
    # Check prerequisites
    if not manager.check_prerequisites():
        logger.info("\n⚠️  Some prerequisites are missing. Install them and try again.")
        return 1
    
    # Validate configuration
    if not manager.validate_configuration():
        logger.error("Configuration validation failed")
        return 1
    
    # Install MCP servers
    if not manager.install_mcp_servers():
        logger.error("MCP server installation failed")
        return 1
    
    # Test server connections
    logger.info("\n🔗 Testing MCP server connections...")
    for server_name in manager.config.get("mcpServers", {}).keys():
        manager.test_server_connection(server_name)
    
    # Generate startup scripts
    if os.name == 'nt':  # Windows
        manager.generate_windows_startup_script()
    else:  # Unix-like
        manager.generate_startup_script()
    
    # Print summary
    manager.print_summary()
    
    logger.info("✅ MCP Infrastructure setup complete!")
    logger.info("Next steps:")
    logger.info("  1. Update .env file with your API keys")
    if os.name == 'nt':
        logger.info("  2. Run: .\\mcp_startup.ps1")
    else:
        logger.info("  2. Run: bash mcp_startup.sh")
    logger.info("  3. Start using content generation scripts\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
