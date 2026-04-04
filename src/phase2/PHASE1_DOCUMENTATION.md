# Phase 1 Documentation

## Overview

Phase 1 of the MCP Deployment Framework establishes the core infrastructure for managing MCP server deployments. This phase delivers four key components that work together to parse manifests, generate Docker configurations, perform health checks, and provide a unified CLI.

## Components

### 1. cli.py - Command Line Interface

**Purpose**: Main entry point for all MCP deployment operations.

**Features**:
- Subcommand-based CLI with argparse
- Four primary commands: `validate`, `generate`, `health`, `list`
- Integrates with manifest parser, Docker generator, and health check system
- Error handling with user-friendly messages

**Usage**:
```bash
# Validate a manifest
python -m src.cli validate manifest.yml

# Generate Docker Compose configuration
python -m src.cli generate manifest1.yml manifest2.yml -o docker-compose.yml

# Run health check
python -m src.cli health manifest.yml

# List manifest details
python -m src.cli list manifest.yml
```

**Key Classes**:
- `MCPDeployCLI`: Main CLI handler
- Command handlers: `_validate_command`, `_generate_command`, `_health_command`, `_list_command`

---

### 2. manifest_parser.py - YAML Manifest Parser

**Purpose**: Parse and validate MCP server manifests from YAML format.

**Features**:
- Validates required fields: `name`, `version`, `runtime`
- Supports multiple runtime types (docker, etc.)
- Parses optional health check configurations
- Handles volumes and environment variables
- Schema validation before object creation

**Manifest Structure**:
```yaml
name: my-mcp-server
version: 1.0.0
runtime: docker
description: Optional description
docker_image: image:tag
port: 8080
health_check:
  type: tcp|http|command
  endpoint: localhost:8080
  timeout_seconds: 30
  interval_seconds: 60
  retries: 3
volumes:
  - source: /host/path
    target: /container/path
environment:
  - name: ENV_VAR
    value: value
```

**Key Classes**:
- `ManifestParser`: Static methods for parsing YAML files and content
- Uses `MCPManifest`, `RuntimeType`, `HealthCheck` from manifest_schema

---

### 3. docker_compose_generator.py - Docker Compose Generator

**Purpose**: Generate Docker Compose configurations from MCP manifests.

**Features**:
- Converts manifest definitions to Docker Compose format
- Supports service configuration: image, entrypoint, command, ports
- Handles volumes (read/write and read-only)
- Configures environment variables
- Generates health check configurations
- Resource constraints (memory limits)
- Multi-manifest aggregation

**Generated Output**:
```yaml
version: '3.8'
services:
  my-mcp-server:
    image: image:tag
    container_name: mcp-my-mcp-server
    ports:
      - "8080:8080"
    healthcheck:
      test: nc -z localhost 8080
      interval: 60s
      timeout: 30s
      retries: 3
```

**Key Classes**:
- `DockerComposeGenerator`: Static methods for generation
- `generate_single()`: Single manifest conversion
- `generate_from_manifests()`: Multi-manifest aggregation
- `_build_health_check()`: Health check configuration builder

---

### 4. health_check.py - Health Check System

**Purpose**: Perform health checks on MCP servers using multiple protocols.

**Features**:
- **TCP checks**: Socket connectivity testing
- **HTTP checks**: HTTP endpoint validation (with requests library or curl fallback)
- **Command checks**: Custom command execution
- **Retry logic**: Configurable retries with interval
- **Timeout handling**: Per-check timeout configuration

**Check Types**:
| Type | Description | Parameters |
|------|-------------|------------|
| TCP | Socket connection | host, port |
| HTTP | HTTP GET request | URL endpoint |
| Command | Shell command | command string |

**Usage**:
```python
from src.health_check import HealthCheckSystem
from src.manifest_schema import HealthCheck, HealthCheckType

# Define health check
hc = HealthCheck(
    type=HealthCheckType.TCP,
    endpoint="localhost:8080",
    timeout_seconds=30,
    retries=3
)

# Run with retries
success, message = HealthCheckSystem.check_with_retry(hc)
```

**Key Classes**:
- `HealthCheckSystem`: Static methods for all check types
- `check_tcp()`, `check_http()`, `check_command()`: Protocol-specific checks
- `perform_health_check()`: Single check execution
- `check_with_retry()`: Retry wrapper with exponential backoff

---

## Integration Flow

```
User CLI Command
      │
      ▼
┌─────────────┐
│   cli.py    │──────────► manifest_parser.py
│  (Entry)    │                │
└─────────────┘                ▼
      │                  Parse YAML
      ▼                    Validate
┌─────────────────┐            │
│ docker_compose_ │◄───────────┘
│  generator.py   │
│  (Generate)     │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  health_check   │
│    (Verify)     │
└─────────────────┘
```

## File Locations

| Component | Path |
|-----------|------|
| CLI | `src/cli.py` |
| Parser | `src/manifest_parser.py` |
| Generator | `src/docker_compose_generator.py` |
| Health Check | `src/health_check.py` |
| Schema | `src/manifest_schema.py` |

## Dependencies

- **Python 3.8+**: Core runtime
- **PyYAML**: YAML parsing
- **requests** (optional): HTTP health checks
- **argparse**: CLI (stdlib)
- **socket**: TCP checks (stdlib)

## Testing

Each component can be tested independently:

```bash
# Test parser
python -c "from src.manifest_parser import ManifestParser; m = ManifestParser.parse_file('test.yml'); print(m)"

# Test generator
python -c "from src.docker_compose_generator import DockerComposeGenerator; print(DockerComposeGenerator.generate_single(manifest))"

# Test health check
python -c "from src.health_check import HealthCheckSystem; print(HealthCheckSystem.check_tcp('localhost:8080'))"
```
