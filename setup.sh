#!/bin/bash
# MCP Deployment Framework Setup Script

set -e

echo "Setting up MCP Deployment Framework..."

# Create virtual environment
python3 -m venv venv || echo "Using existing Python environment"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Install dependencies
pip install -r requirements.txt

# Make CLI executable
chmod +x scripts/mcp-deploy

echo "Setup complete!"
echo ""
echo "Usage examples:"
echo "  ./scripts/mcp-deploy validate manifests/filesystem-server.yaml"
echo "  ./scripts/mcp-deploy generate manifests/*.yaml -o docker-compose.yml"
echo "  ./scripts/mcp-deploy health manifests/filesystem-server.yaml"
echo "  ./scripts/mcp-deploy list manifests/*.yaml"
