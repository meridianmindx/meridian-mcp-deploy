# Configuration Guide - meridian-mcp-deploy

Comprehensive guide to configuring MCP deployments.

## Manifest Configuration

### Basic Manifest

```yaml
name: my-mcp-server
version: "1.0.0"
runtime: python
port: 8080
description: My MCP server
```

### Complete Manifest

```yaml
name: complete-mcp-server
version: "1.0.0"
runtime: python
port: 8080
description: Complete MCP server configuration

# Health check
health_check:
  type: http
  endpoint: /health
  timeout: 10
  interval: 30
  retries: 3

# Volumes
volumes:
  - ./data:/app/data
  - server-cache:/app/cache

# Environment variables
environment:
  - LOG_LEVEL=INFO
  - MAX_CONNECTIONS=100
  - DATABASE_URL=postgresql://localhost:5432/db

# Dependencies
depends_on:
  - postgres-server
  - redis-server

# Networks
networks:
  - mcp-backend
  - mcp-frontend

# Labels
labels:
  team: platform
  environment: production

# Resources
resources:
  limits:
    cpu: "1.0"
    memory: "1G"
  reservations:
    cpu: "0.5"
    memory: "512M"
```

## Health Check Configuration

### HTTP Health Check

```yaml
health_check:
  type: http
  endpoint: /health
  method: GET
  expected_status: 200
  timeout: 10
  interval: 30
  retries: 3
```

### TCP Health Check

```yaml
health_check:
  type: tcp
  port: 8080
  timeout: 5
  retries: 3
```

### Custom Script Health Check

```yaml
health_check:
  type: script
  script: ./scripts/health-check.sh
  timeout: 15
  retries: 3
```

## Volume Configuration

### Bind Mounts

```yaml
volumes:
  - ./data:/app/data
  - ./config:/app/config:ro  # Read-only
```

### Named Volumes

```yaml
volumes:
  - server-data:/app/data
  - server-cache:/app/cache

volumes:
  server-data:
    driver: local
  server-cache:
    driver: local
```

## Environment Variables

### Inline Definition

```yaml
environment:
  - LOG_LEVEL=INFO
  - MAX_CONNECTIONS=100
  - DATABASE_URL=postgresql://user:pass@host:5432/db
```

### From .env File

```yaml
env_file:
  - .env
  - .env.production
```

### From Secrets

```yaml
secrets:
  - api_key
  - db_password

environment:
  - API_KEY_FILE=/run/secrets/api_key
```

## Network Configuration

### Custom Networks

```yaml
networks:
  mcp-frontend:
    driver: bridge
  mcp-backend:
    driver: bridge
    internal: true  # No external access
```

### Network Aliases

```yaml
services:
  my-server:
    networks:
      mcp-backend:
        aliases:
          - api-server
          - backend-service
```

## Resource Configuration

### CPU and Memory Limits

```yaml
resources:
  limits:
    cpus: '1.0'
    memory: 1G
  reservations:
    cpus: '0.5'
    memory: 512M
```

### GPU Resources

```yaml
resources:
  limits:
    cpus: '2.0'
    memory: 2G
    devices:
      - driver: nvidia
        count: 1
        capabilities: [gpu]
```

## Restart Policies

```yaml
restart: on-failure
# or
restart: always
# or
restart: unless-stopped
```

### Advanced Restart Configuration

```yaml
deploy:
  restart_policy:
    condition: on-failure
    delay: 5s
    max_attempts: 3
    window: 120s
```

## Logging Configuration

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
    compress: "true"
```

## Labels and Metadata

```yaml
labels:
  team: platform
  environment: production
  version: "1.0.0"
  owner: devops-team
```

## Best Practices

1. **Use semantic versioning** for version numbers
2. **Define health checks** for all services
3. **Set resource limits** to prevent runaway containers
4. **Use named volumes** for persistent data
5. **Separate networks** for frontend and backend
6. **Use environment variables** for configuration
7. **Implement proper logging** for debugging

## Related Resources

- [API Reference](./api-reference.md)
- [Troubleshooting](./troubleshooting.md)
- [FAQ](./faq.md)
