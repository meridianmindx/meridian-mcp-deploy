# API Reference - meridian-mcp-deploy

Complete API documentation for MCP Deploy Framework.

## Table of Contents

- [CLI Commands](#cli-commands)
- [ManifestParser](#manifestparser)
- [DockerComposeGenerator](#dockercomposegenerator)
- [HealthCheckSystem](#healthchecksystem)
- [Manifest Schema](#manifest-schema)

---

## CLI Commands

### Validate

```bash
meridian-mcp-deploy validate <manifest>
```

Validate a manifest file.

**Example:**
```bash
meridian-mcp-deploy validate manifests/filesystem-server.yaml
```

**Output:**
```
✓ Manifest 'filesystem-server' v1.0.0 is valid
 Runtime: python
 Description: MCP filesystem server
```

### Generate

```bash
meridian-mcp-deploy generate <manifests...> -o <output>
```

Generate Docker Compose configuration from manifests.

**Example:**
```bash
meridian-mcp-deploy generate manifest1.yaml manifest2.yaml -o docker-compose.yml
```

**Output:**
```
✓ Parsed manifest: filesystem-server
✓ Parsed manifest: playwright-server
✓ Generated Docker Compose configuration: docker-compose.yml
 Services: filesystem-server, playwright-server
```

### Health

```bash
meridian-mcp-deploy health <manifest> [--retries N]
```

Perform health check on a deployed server.

**Example:**
```bash
meridian-mcp-deploy health manifests/filesystem-server.yaml --retries 3
```

**Output:**
```
Performing health check for filesystem-server...
✓ Health check passed: HTTP 200 OK
```

### List

```bash
meridian-mcp-deploy list <manifests...>
```

List parsed manifest details.

**Example:**
```bash
meridian-mcp-deploy list *.yaml
```

---

## ManifestParser

Parse and validate MCP server manifests.

### parse_file(filepath)

```python
from manifest_parser import ManifestParser

manifest = ManifestParser.parse_file('manifest.yaml')
```

**Returns:** Manifest object

### Manifest Object

```python
manifest.name          # str: Server name
manifest.version       # str: Version
manifest.runtime       # Runtime enum (python/node)
manifest.port          # int: Port number
manifest.description   # str: Description
manifest.health_check  # HealthCheck config
manifest.volumes       # List[str]: Volume mappings
manifest.environment   # List[str]: Environment variables
```

---

## DockerComposeGenerator

Generate Docker Compose configurations.

### generate_from_manifests(manifests)

```python
from docker_compose_generator import DockerComposeGenerator

compose_config = DockerComposeGenerator.generate_from_manifests([manifest1, manifest2])
```

**Returns:** Dict containing compose configuration

### write_compose_file(config, output_path)

```python
DockerComposeGenerator.write_compose_file(compose_config, 'docker-compose.yml')
```

---

## HealthCheckSystem

Perform health checks on deployed servers.

### check_with_retry(health_config, max_retries=3)

```python
from health_check import HealthCheckSystem

success, message = HealthCheckSystem.check_with_retry(health_config, max_retries=3)
```

**Returns:** Tuple[bool, str]

### check_http(endpoint, timeout=10)

```python
success, message = HealthCheckSystem.check_http('http://localhost:8080/health', timeout=10)
```

### check_tcp(host, port, timeout=5)

```python
success, message = HealthCheckSystem.check_tcp('localhost', 8080, timeout=5)
```

---

## Manifest Schema

### Required Fields

```yaml
name: string        # Server name (alphanumeric, hyphens)
version: string     # Semver version
runtime: string     # 'python' or 'node'
```

### Optional Fields

```yaml
port: number                    # Port number (default: 8080)
description: string            # Server description
health_check: object           # Health check configuration
volumes: array                 # Volume mappings
environment: array             # Environment variables
depends_on: array              # Service dependencies
networks: array                # Network configurations
labels: object                 # Docker labels
resources: object              # Resource limits
```

### Health Check Schema

```yaml
health_check:
  type: string          # 'http', 'tcp', or 'script'
  endpoint: string      # Health check endpoint (http)
  port: number          # Port for TCP checks
  timeout: number       # Timeout in seconds
  interval: number      # Check interval
  retries: number       # Number of retries
  script: string        # Script path (script type)
```

---

## Examples

### Basic Usage

```python
from manifest_parser import ManifestParser
from docker_compose_generator import DockerComposeGenerator

# Parse manifest
manifest = ManifestParser.parse_file('manifest.yaml')

# Generate compose config
compose = DockerComposeGenerator.generate_from_manifests([manifest])

# Write to file
DockerComposeGenerator.write_compose_file(compose, 'docker-compose.yml')
```

### Health Check

```python
from health_check import HealthCheckSystem

# HTTP health check
success, message = HealthCheckSystem.check_http('http://localhost:8080/health')

# TCP health check
success, message = HealthCheckSystem.check_tcp('localhost', 8080)

# With retries
success, message = HealthCheckSystem.check_with_retry(health_config, max_retries=3)
```

### Custom Manifest

```yaml
name: custom-server
version: "1.0.0"
runtime: python
port: 8080
description: Custom MCP server

health_check:
  type: http
  endpoint: /health
  timeout: 10

volumes:
  - ./data:/app/data

environment:
  - LOG_LEVEL=INFO
  - MAX_CONNECTIONS=100

resources:
  cpu: "1.0"
  memory: "1G"
```

---

## Error Handling

```python
from manifest_parser import ManifestParser
from manifest_schema import ManifestValidationError

try:
    manifest = ManifestParser.parse_file('invalid.yaml')
except ManifestValidationError as e:
    print(f"Validation error: {e}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Related Resources

- [Configuration Guide](./configuration.md)
- [Troubleshooting](./troubleshooting.md)
- [FAQ](./faq.md)
