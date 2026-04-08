# Getting Started with MCP Deploy in 5 Minutes

**Skill Level**: Beginner  
**Time Required**: 5 minutes  
**What You'll Build**: A working MCP server deployment

## Overview

This tutorial will guide you through deploying an MCP server using manifest-based configuration. By the end, you'll have a production-ready Docker deployment.

## Prerequisites

- Python 3.9+ installed
- Docker installed
- Basic YAML knowledge

## Step 1: Installation (1 minute)

```bash
# Install from PyPI (coming soon)
pip install meridian-mcp-deploy

# Or install from source
git clone https://github.com/meridian/meridian-mcp-deploy.git
cd meridian-mcp-deploy-framework
pip install -e .
```

**Expected output:**
```bash
Successfully installed meridian-mcp-deploy-1.0.0
```

## Step 2: Create a Manifest (1 minute)

Create `my-server.yaml`:

```yaml
name: my-mcp-server
version: "1.0.0"
runtime: python
port: 8080
description: My first MCP server
health_check:
  type: http
  endpoint: /health
  timeout: 10
```

## Step 3: Validate (1 minute)

```bash
meridian-mcp-deploy validate my-server.yaml
```

**Expected output:**
```bash
✓ Manifest 'my-mcp-server' v1.0.0 is valid
 Runtime: python
 Description: My first MCP server
```

## Step 4: Generate Deployment (1 minute)

```bash
meridian-mcp-deploy generate my-server.yaml -o docker-compose.yml
```

**Expected output:**
```bash
✓ Parsed manifest: my-mcp-server
✓ Generated Docker Compose configuration: docker-compose.yml
 Services: my-mcp-server
```

## Step 5: Deploy (1 minute)

```bash
docker-compose up -d
```

**Expected output:**
```bash
[+] Running 2/2
 ✔ Container my-mcp-server    Created
 ✔ Network mcp-default        Created
```

## What You've Learned

- ✅ How to create an MCP server manifest
- ✅ How to validate manifest syntax
- ✅ How to generate Docker configurations
- ✅ How to deploy with Docker Compose

## What's Next

- [Deep Dive Tutorial](./deep-dive.md) - Advanced features
- [API Reference](../docs/api-reference.md) - Complete documentation
- [Common Use Cases](../docs/use-cases.md) - Real-world examples

## Troubleshooting

**Issue**: "meridian-mcp-deploy: command not found"
- **Solution**: Run `pip install -e .` in the project directory

**Issue**: "Docker not found"
- **Solution**: Install Docker Desktop or Docker Engine

**Issue**: "Manifest validation failed"
- **Solution**: Check YAML syntax and required fields

**Estimated Time**: 5 minutes  
**Time Saved**: 15-30 minutes per deployment
