# Quick Start Demo - MCP Deploy

This demo shows how to deploy MCP servers with one command in under 2 minutes.

## What This Solves

- **Problem**: Manually creating Docker configurations for MCP servers is tedious
- **Solution**: One-command deployment with manifest-based configuration
- **Time Saved**: 15-30 minutes per server deployment
- **Cost Savings**: Reduced deployment errors and faster iteration

## Prerequisites

- Python 3.9+
- Docker installed
- MCP server manifest file

## Installation

```bash
# Install from PyPI (coming soon)
pip install meridian-mcp-deploy

# Or install from source
git clone https://github.com/meridian/meridian-mcp-deploy.git
cd meridian-mcp-deploy-framework
pip install -e .
```

## Basic Example

### Step 1: Create a Manifest

Create `filesystem-server.yaml`:

```yaml
name: filesystem-server
version: "1.0.0"
runtime: python
port: 8080
description: MCP server for file system operations
health_check:
  type: http
  endpoint: /health
  timeout: 10
```

### Step 2: Validate the Manifest

```bash
meridian-mcp-deploy validate filesystem-server.yaml
```

**Expected output:**
```bash
✓ Manifest 'filesystem-server' v1.0.0 is valid
 Runtime: python
 Description: MCP server for file system operations
```

### Step 3: Generate Docker Compose

```bash
meridian-mcp-deploy generate filesystem-server.yaml -o docker-compose.yml
```

**Expected output:**
```bash
✓ Parsed manifest: filesystem-server
✓ Generated Docker Compose configuration: docker-compose.yml
 Services: filesystem-server
```

### Step 4: Deploy

```bash
docker-compose up -d
```

**Expected output:**
```bash
[+] Running 2/2
 ✔ Container filesystem-server    Created
 ✔ Network mcp-default            Created
```

## Generated Files

The generated `docker-compose.yml` includes:

```yaml
version: '3.8'

services:
  filesystem-server:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: filesystem-server
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

## Health Check

```bash
meridian-mcp-deploy health filesystem-server.yaml --retries 3
```

**Expected output:**
```bash
Performing health check for filesystem-server...
✓ Health check passed: HTTP 200 OK
```

## Next Steps

- Try the [Advanced Usage Demo](./advanced-usage.md) for multi-server deployment
- Read the [Getting Started Tutorial](../tutorials/getting-started-5-minutes.md)
- Explore [API Reference](../docs/api-reference.md)

**Estimated Runtime**: 2 minutes
**Time Saved**: 15-30 minutes per deployment
