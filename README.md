# MCP Deploy Framework

[![PyPI version](https://img.shields.io/pypi/v/meridian-mcp-deploy.svg)](https://pypi.org/project/meridian-mcp-deploy/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://github.com/meridianmindx/meridian-mcp-deploy/actions/workflows/build.yml/badge.svg)](https://github.com/meridianmindx/meridian-mcp-deploy/actions/workflows/build.yml) [![PyPI downloads](https://img.shields.io/pypi/dm/meridian-mcp-deploy.svg)](https://pypi.org/project/meridian-mcp-deploy/) [![GitHub stars](https://img.shields.io/github/stars/meridianmindx/meridian-mcp-deploy.svg?style=social)](https://github.com/meridianmindx/meridian-mcp-deploy/stargazers)

**Deploy MCP servers with one command.** Generate Docker configurations, validate manifests, and perform health checks for Model Context Protocol (MCP) servers. Perfect for developers building AI agent infrastructure.

## ⭐ Why this matters
- Save hours of manual Docker configuration
- Ensure your MCP server meets deployment standards
- Built for the growing MCP ecosystem (3,858+ servers)
- Production-ready with health checks and monitoring

## 🚀 Quick Start

```bash
# Install
pip install meridian-mcp-deploy

# Validate a manifest
meridian-mcp-deploy validate manifests/filesystem-server.yaml

# Generate Docker Compose configuration
meridian-mcp-deploy generate manifests/filesystem-server.yaml manifests/playwright-server.yaml -o docker-compose.yml

# Run health check
meridian-mcp-deploy health manifests/filesystem-server.yaml
```

## 📦 Installation

```bash
# From PyPI (recommended)
pip install meridian-mcp-deploy

# From source (for development)
git clone https://github.com/meridianmindx/meridian-mcp-deploy.git
cd meridian-mcp-deploy
pip install -e ".[dev]"
```

## ✨ Features

- **Manifest Validation**: YAML schema validation for MCP server definitions
- **Docker Compose Generation**: Auto-generate optimized container configurations
- **Health Check System**: HTTP, TCP, and stdio protocol support with retries
- **Dependency Resolution**: Python import → apt package mapping (Phase 2)
- **Connectivity Validator**: Test server connectivity before deployment (Phase 2)

## 📖 Usage Examples

### Validate a Manifest

```bash
meridian-mcp-deploy validate manifests/filesystem-server.yaml
```

Output:
```
✓ Manifest 'filesystem-server' v1.0.0 is valid
 Runtime: python
 Description: MCP filesystem server for file operations
```

### Generate Docker Compose

```bash
meridian-mcp-deploy generate manifests/filesystem-server.yaml -o docker-compose.yml
```

Output:
```
✓ Parsed manifest: filesystem-server
✓ Generated Docker Compose configuration: docker-compose.yml
 Services: filesystem-server
```

### Perform Health Check

```bash
meridian-mcp-deploy health manifests/filesystem-server.yaml --retries 3
```

Output:
```
Performing health check for filesystem-server...
✓ Health check passed: HTTP 200 OK
```

## 📁 Example Manifests

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

## 🛠️ CLI Commands

| Command | Description |
|---------|-------------|
| `meridian-mcp-deploy validate <manifest>` | Validate manifest YAML file |
| `meridian-mcp-deploy generate <manifests...> -o <output>` | Generate Docker Compose config |
| `meridian-mcp-deploy health <manifest> [--retries N]` | Perform health check |
| `meridian-mcp-deploy list <manifests...>` | List parsed manifest details |

## 📂 Project Structure

```
meridian-mcp-deploy/
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

## 🗺️ Roadmap

- [x] Phase 1: Core CLI, manifest parser, Docker generator, health checks
- [x] Phase 2: Dependency resolver, connectivity validator
- [ ] PyPI package publication
- [ ] Kubernetes manifest generation
- [ ] Multi-server orchestration
- [ ] Web UI for manifest editing
- [ ] Enterprise features (RBAC, audit logs)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🌐 Community

- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Share ideas and ask questions
- **MCP Discord**: Join the Model Context Protocol community

---

## ❤️ Support this project

If this tool helps you deploy MCP servers faster, please consider **starring this repository** on GitHub. Stars help other developers discover useful tools!

[⭐ Star this repo](https://github.com/meridianmindx/meridian-mcp-deploy/stargazers) • [💬 Start a discussion](https://github.com/meridianmindx/meridian-mcp-deploy/discussions) • [🐛 Report issues](https://github.com/meridianmindx/meridian-mcp-deploy/issues)

**Built for the MCP ecosystem** • [awesome-mcp-servers](https://github.com/modelcontextprotocol/servers) has 3,858+ stars

## 💰 Affiliate Disclosure

We participate in affiliate programs for cloud providers. If you sign up using our links, we may earn a commission at no extra cost to you. This helps support the project.

- **AWS**: [Sign up for AWS Free Tier](https://aws.amazon.com/free/?tag=meridian-20)
- **DigitalOcean**: [Get $200 credit](https://m.do.co/c/meridian-20)
- **GCP**: [Start with $300 free](https://cloud.google.com/free/?utm_source=meridian)

These links provide you with the same great deals and help us continue building open-source tools.