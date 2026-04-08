# Advanced Usage Demo - Multi-Server Deployment

This demo demonstrates deploying multiple MCP servers with dependency management and health monitoring.

## What This Solves

- **Problem**: Managing multiple MCP servers with different configurations
- **Solution**: Unified deployment with automatic dependency resolution
- **Time Saved**: 1-2 hours per multi-server deployment
- **Cost Savings**: Reduced operational overhead and faster scaling

## Features Demonstrated

1. Multi-server manifest parsing
2. Dependency resolution
3. Network orchestration
4. Health check integration
5. Volume management

## Complete Example

### Step 1: Create Multiple Manifests

**filesystem-server.yaml:**
```yaml
name: filesystem-server
version: "1.0.0"
runtime: python
port: 8080
description: MCP filesystem server
health_check:
  type: http
  endpoint: /health
  timeout: 10
volumes:
  - ./data:/app/data
```

**playwright-server.yaml:**
```yaml
name: playwright-server
version: "1.0.0"
runtime: node
port: 3000
description: MCP browser automation server
health_check:
  type: http
  endpoint: /health
  timeout: 15
depends_on:
  - filesystem-server
```

**context-server.yaml:**
```yaml
name: context-server
version: "1.0.0"
runtime: python
port: 5000
description: MCP context management server
health_check:
  type: http
  endpoint: /health
  timeout: 10
depends_on:
  - filesystem-server
```

### Step 2: Validate All Manifests

```bash
for manifest in *.yaml; do
  meridian-mcp-deploy validate $manifest
done
```

**Expected output:**
```bash
✓ Manifest 'filesystem-server' v1.0.0 is valid
✓ Manifest 'playwright-server' v1.0.0 is valid
✓ Manifest 'context-server' v1.0.0 is valid
```

### Step 3: Generate Unified Deployment

```bash
meridian-mcp-deploy generate filesystem-server.yaml playwright-server.yaml context-server.yaml -o docker-compose.yml
```

**Expected output:**
```bash
✓ Parsed manifest: filesystem-server
✓ Parsed manifest: playwright-server
✓ Parsed manifest: context-server
✓ Generated Docker Compose configuration: docker-compose.yml
 Services: filesystem-server, playwright-server, context-server
```

### Step 4: Deploy with Dependencies

```bash
docker-compose up -d
```

**Expected output:**
```bash
[+] Running 5/5
 ✔ Network mcp-network              Created
 ✔ Volume "mcp_data"                Created
 ✔ Container filesystem-server      Started
 ✔ Container playwright-server      Started
 ✔ Container context-server         Started
```

### Step 5: Verify Health

```bash
docker-compose ps
```

**Expected output:**
```bash
NAME                    STATUS             HEALTH
filesystem-server       Up (healthy)       3/3 OK
playwright-server       Up (healthy)       3/3 OK
context-server          Up (healthy)       3/3 OK
```

## Generated Docker Compose

```yaml
version: '3.8'

services:
  filesystem-server:
    build:
      context: ./filesystem-server
      dockerfile: Dockerfile
    container_name: filesystem-server
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
      - filesystem-data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - mcp-network

  playwright-server:
    build:
      context: ./playwright-server
      dockerfile: Dockerfile
    container_name: playwright-server
    ports:
      - "3000:3000"
    depends_on:
      filesystem-server:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 15s
      retries: 3
    networks:
      - mcp-network

  context-server:
    build:
      context: ./context-server
      dockerfile: Dockerfile
    container_name: context-server
    ports:
      - "5000:5000"
    depends_on:
      filesystem-server:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - mcp-network

volumes:
  filesystem-data:
    driver: local

networks:
  mcp-network:
    driver: bridge
```

## Terminal Session Example

```bash
$ meridian-mcp-deploy generate *.yaml -o docker-compose.yml
✓ Parsed manifest: filesystem-server
✓ Parsed manifest: playwright-server
✓ Parsed manifest: context-server
✓ Generated Docker Compose configuration: docker-compose.yml
 Services: filesystem-server, playwright-server, context-server

$ docker-compose up -d
[+] Running 5/5
 ✔ Network mcp-network              Created
 ✔ Volume "mcp_data"                Created
 ✔ Container filesystem-server      Started
 ✔ Container playwright-server      Started
 ✔ Container context-server         Started

$ docker-compose ps
NAME                    STATUS             HEALTH
filesystem-server       Up (healthy)       3/3 OK
playwright-server       Up (healthy)       3/3 OK
context-server          Up (healthy)       3/3 OK

$ meridian-mcp-deploy health filesystem-server.yaml
Performing health check for filesystem-server...
✓ Health check passed: HTTP 200 OK
```

## Key Takeaways

- **Manifest-based deployment**: Simple YAML configuration
- **Automatic dependency management**: Services start in correct order
- **Health monitoring**: Built-in health checks for all services
- **Unified networking**: All servers on same network

## Related Resources

- [Quick Start Demo](./quick-start.md)
- [API Reference](../docs/api-reference.md)
- [Configuration Guide](../docs/configuration.md)

**Estimated Runtime**: 5 minutes
**Time Saved**: 1-2 hours per deployment
