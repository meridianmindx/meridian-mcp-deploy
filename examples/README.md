# MCP Deploy Framework Examples

This directory contains example MCP server manifests for testing and learning.

## Quick Start

```bash
# Validate an example manifest
meridian-mcp-deploy validate manifests/filesystem-server.yaml

# Generate Docker Compose configuration
meridian-mcp-deploy generate manifests/filesystem-server.yaml -o docker-compose.yml

# View generated configuration
cat docker-compose.yml
```

## Example Manifests

See the parent `manifests/` directory for example YAML files:

1. **filesystem-server.yaml** - Basic MCP filesystem server
2. **playwright-server.yaml** - Browser automation server  
3. **custom-server.yaml** - Template for custom deployments

## Testing Commands

```bash
# Validate all examples
meridian-mcp-deploy validate manifests/filesystem-server.yaml
meridian-mcp-deploy validate manifests/playwright-server.yaml

# Generate multi-service deployment
meridian-mcp-deploy generate manifests/*.yaml -o multi-service-compose.yml

# List manifest details
meridian-mcp-deploy list manifests/*.yaml
```
