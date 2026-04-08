# MCP Deploy Framework

[![Python 3.9+](https://img.shields.io/bpython/3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**One-command deployment for MCP servers.** Generate Docker Compose configurations, validate manifests, and perform health checks for Model Context Protocol (MCP) servers.

## Quick Start

```bash
# Install
pip install meridian-mcp-deploy  # Coming soon - or clone this repo

# Validate a manifest
meridian-mcp-deploy validate manifests/filesystem-server.yaml

# Generate Docker Compose configuration
meridian-mcp-deploy generate manifests/filesystem-server.yaml manifests/playwright-server.yaml -o docker-compose.yml

# Run health check
meridian-mcp-deploy health manifests/filesystem-server.yaml
```

## Features

- **Manifest Validation**: YAML schema validation for MCP server definitions
- **Docker Compose Generation**: Auto-generate optimized container configurations
- **Health Check System**: HTTP, TCP, and stdio protocol support with retries
- **Dependency Resolution**: Python import → apt package mapping (Phase 2)
- **Connectivity Validator**: Test server connectivity before deployment (Phase 2)

## Installation

```bash
# From source
git clone https://github.com/meridian-mind/mcp-deploy.git
cd mcp-deploy-framework
pip install -r requirements.txt

# Or via pip (coming soon)
pip install meridian-mcp-deploy
```

## Usage

### 1. Validate a Manifest

```bash
mcp-deploy validate manifests/filesystem-server.yaml
```

Output:
```
✓ Manifest 'filesystem-server' v1.0.0 is valid
 Runtime: python
 Description: MCP filesystem server for file operations
```

### 2. Generate Docker Compose

```bash
mcp-deploy generate manifests/filesystem-server.yaml -o docker-compose.yml
```

Output:
```
✓ Parsed manifest: filesystem-server
✓ Generated Docker Compose configuration: docker-compose.yml
 Services: filesystem-server
```

### 3. Perform Health Check

```bash
mcp-deploy health manifests/filesystem-server.yaml --retries 3
```

Output:
```
Performing health check for filesystem-server...
✓ Health check passed: HTTP 200 OK
```

## Example Manifests

### Filesystem Server

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

### Playwright Server

```yaml
name: playwright-server
version: "1.0.0"
runtime: node
port: 3000
description: MCP server for browser automation
health_check:
  type: http
  endpoint: /health
  timeout: 15
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `meridian-mcp-deploy validate <manifest>` | Validate manifest YAML file |
| `meridian-mcp-deploy generate <manifests...> -o <output>` | Generate Docker Compose config |
| `meridian-mcp-deploy health <manifest> [--retries N]` | Perform health check |
| `meridian-mcp-deploy list <manifests...>` | List parsed manifest details |

## Project Structure

```
mcp-deploy-framework/
├── src/
│   ├── cli.py                 # Command-line interface
│   ├── manifest_parser.py     # YAML manifest parsing
│   ├── manifest_schema.py     # JSON schema validation
│   ├── docker_compose_generator.py  # Docker Compose generation
│   ├── health_check.py        # Health check system
│   └── phase2/
│       ├── dependency_resolver.py    # Import → apt mapping
│       └── mcp_connectivity_validator.py  # Connectivity testing
├── manifests/                 # Example manifests
├── tests/                     # Test suite
├── docs/                      # Documentation
└── scripts/                   # Utility scripts
```

## Roadmap

- [x] Phase 1: Core CLI, manifest parser, Docker generator, health checks
- [x] Phase 2: Dependency resolver, connectivity validator
- [ ] PyPI package publication
- [ ] Kubernetes manifest generation
- [ ] Multi-server orchestration
- [ ] Web UI for manifest editing
- [ ] Enterprise features (RBAC, audit logs)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Community

- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Share ideas and ask questions
- **MCP Discord**: Join the Model Context Protocol community

---

**Built for the MCP ecosystem** • [awesome-mcp-servers](https://github.com/modelcontextprotocol/servers) has 3,858+ stars
