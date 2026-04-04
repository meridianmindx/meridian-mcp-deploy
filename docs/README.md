# MCP Server Deployment Framework - Phase 1

A framework for deploying Model Context Protocol (MCP) servers with automated Docker Compose generation and health checking.

## Features

- **Manifest Parser**: Parse and validate MCP server YAML manifests
- **Schema Validation**: Enforce required fields and validate configurations
- **Docker Compose Generator**: Auto-generate Docker Compose configurations
- **Health Check System**: Perform connectivity tests for MCP servers
- **CLI Interface**: Simple command-line interface for all operations

## Quick Start

1. Install dependencies:
   ```bash
   ./setup.sh
   ```

2. Validate a manifest:
   ```bash
   ./scripts/mcp-deploy validate manifests/filesystem-server.yaml
   ```

3. Generate Docker Compose file:
   ```bash
   ./scripts/mcp-deploy generate manifests/*.yaml -o docker-compose.yml
   ```

4. Perform health check:
   ```bash
   ./scripts/mcp-deploy health manifests/filesystem-server.yaml
   ```

## Manifest Schema

### Required Fields
- `name`: Server name (string)
- `version`: Version string (semantic versioning recommended)
- `runtime`: One of: `docker`, `node`, `python`, `binary`

### Docker Runtime Fields
- `docker_image`: Docker image name and tag
- `entrypoint`: Container entrypoint (optional)
- `command`: Command to run (optional)

### Optional Fields
- `port`: Port number for the service
- `host`: Hostname (default: localhost)
- `memory_limit`: Memory limit (e.g., "512m", "1g")
- `cpu_shares`: CPU shares
- `description`: Service description
- `maintainer`: Maintainer information
- `license`: License type

### Health Check Configuration
```yaml
health_check:
  type: http | tcp | command
  endpoint: "http://localhost:8080/health"  # for http/tcp
  command: "echo healthy"  # for command
  timeout_seconds: 30
  interval_seconds: 60
  retries: 3
```

### Volume Mounts
```yaml
volumes:
  - source: ./workspace
    target: /workspace
    read_only: false
```

### Environment Variables
```yaml
environment:
  - name: LOG_LEVEL
    value: INFO
    secret: false
  - name: API_KEY
    value: ${API_KEY}
    secret: true
```

## Architecture

```
mcp-deploy-framework/
├── src/
│   ├── manifest_schema.py    # Data classes and validation
│   ├── manifest_parser.py    # YAML parsing
│   ├── docker_compose_generator.py  # Compose file generation
│   ├── health_check.py       # Health check system
│   └── cli.py               # Command-line interface
├── manifests/               # Example manifests
├── scripts/                # CLI wrapper
├── tests/                  # Unit tests
└── docs/                   # Documentation
```

## Examples

See `manifests/` directory for example configurations:
- `filesystem-server.yaml`: Filesystem MCP server
- `playwright-server.yaml`: Playwright browser automation server

## Phase 1 Deliverables

✅ Manifest parser with YAML validation  
✅ Basic schema validator  
✅ Docker Compose generator  
✅ Health check system  
✅ Sample manifests  
✅ CLI interface  
✅ Setup scripts  
✅ Documentation  

## Next Steps (Future Phases)

1. **Phase 2**: Multi-runtime support (Node.js, Python binaries)
2. **Phase 3**: Kubernetes manifest generation
3. **Phase 4**: Monitoring and metrics integration
4. **Phase 5**: CI/CD pipeline automation

## License

MIT License - See LICENSE file for details.
