# 🚀 MCP Deploy Framework

<div align="center">

[![PyPI version](https://img.shields.io/pypi/v/meridian-mcp-deploy.svg)](https://pypi.org/project/meridian-mcp-deploy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/meridianmindx/meridian-mcp-deploy/actions/workflows/build.yml/badge.svg)](https://github.com/meridianmindx/meridian-mcp-deploy/actions/workflows/build.yml)
[![PyPI downloads](https://img.shields.io/pypi/dm/meridian-mcp-deploy.svg)](https://pypi.org/project/meridian-mcp-deploy/)
[![GitHub Repo stars](https://img.shields.io/github/stars/meridianmindx/meridian-mcp-deploy?style=social&label=Star)](https://github.com/meridianmindx/meridian-mcp-deploy/stargazers)
[![Meridian Tooling](https://img.shields.io/badge/Part_of-Meridian_Tooling_Suite-3498db)](https://github.com/meridianmindx)

<!-- Star CTA -->
<div>

## ⭐ Star This Repo!

**If this tool saves you time deploying MCP servers, please star it!** Stars help other developers discover useful tools.

[![Star us on GitHub](https://img.shields.io/badge/-⭐_Star_this_repo-black?style=for-the-badge&logo=github)](https://github.com/meridianmindx/meridian-mcp-deploy/stargazers)

</div>

<!-- Try It Now -->
<div>

## 🚀 Try It Now

[![Open in GitHub Codespaces](https://img.shields.io/badge/Open%20in%20GitHub%20Codespaces-blue?logo=github)](https://codespaces.new/meridianmindx/meridian-mcp-deploy)
[![Try on Replit](https://img.shields.io/badge/Try%20on%20Replit-black?logo=replit)](https://replit.com/@meridianmindx/meridian-mcp-deploy)
[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/meridianmindx/meridian-mcp-deploy/HEAD)

</div>

</div>

---

## 📋 Table of Contents
- [Why This Tool Matters](#-why-this-tool-matters)
- [Quick Start](#-quick-start)
- [Features](#-features)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Community](#-community)
- [Contributing](#-contributing)
- [License](#-license)
- [See Also](#-see-also)

## 🔥 Why This Tool Matters

**Deploy MCP servers with one command.** Save hours of manual Docker configuration for Model Context Protocol (MCP) servers.

- ✅ **Save 2-3 hours per deployment** – Automate repetitive Docker config work
- ✅ **Built for the growing MCP ecosystem** – 3,858+ MCP servers and counting
- ✅ **Production-ready** – Health checks, monitoring, and validation included
- ✅ **Open source** – MIT licensed, community-driven

## ⚡ Quick Start

```bash
# Install
pip install meridian-mcp-deploy

# Validate a manifest
meridian-mcp-deploy validate manifests/filesystem-server.yaml

# Generate Docker Compose config
meridian-mcp-deploy generate manifests/filesystem-server.yaml -o docker-compose.yml

# Run health check
meridian-mcp-deploy health manifests/filesystem-server.yaml --retries 3
```

## 🎯 Features

| Feature | Description | Status |
|---------|-------------|--------|
| Manifest Validation | YAML schema validation for MCP server definitions | ✅ Live |
| Docker Compose Generation | Auto-generate optimized container configurations | ✅ Live |
| Health Check System | HTTP, TCP, and stdio protocol support with retries | ✅ Live |
| Dependency Resolution | Python import → apt package mapping | 🔄 Phase 2 |
| Connectivity Testing | Test server connectivity before deployment | 🔄 Phase 2 |

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install meridian-mcp-deploy
```

### From Source
```bash
git clone https://github.com/meridianmindx/meridian-mcp-deploy.git
cd meridian-mcp-deploy
pip install -e .[dev]
```

## 📖 Usage Examples

### Example 1: Full Deployment Pipeline
```bash
# 1. Validate your manifest
meridian-mcp-deploy validate my-mcp-server.yaml

# 2. Generate Docker configuration
meridian-mcp-deploy generate my-mcp-server.yaml -o docker-compose.prod.yml

# 3. Test connectivity
meridian-mcp-deploy health my-mcp-server.yaml --timeout 30

# 4. Deploy!
docker-compose -f docker-compose.prod.yml up -d
```

### Example 2: Batch Processing
```bash
# Process multiple manifests
for manifest in manifests/*.yaml; do
  meridian-mcp-deploy validate "$manifest"
  meridian-mcp-deploy generate "$manifest" -o "output/${manifest##*/}.yml"
done
```

## 👥 Community

### Recent Activity
- **Issues**: 4 open | 2 closed
- **Pull Requests**: 1 open | 0 merged
- **Discussions**: 3 active threads

### Get Involved
1. **Star the repo** – Help others discover this tool
2. **Join discussions** – Share ideas and feedback
3. **Report issues** – Help improve the project
4. **Submit PRs** – Contribute features or fixes

[![Join our GitHub Discussions](https://img.shields.io/badge/Join%20Discussions-181717?style=for-the-badge&logo=github)](https://github.com/meridianmindx/meridian-mcp-deploy/discussions)

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 See Also

**Part of the Meridian Tooling Suite** – Complementary tools for AI agent development:

### 🚀 [Meridian CrewAI Agent Deployment Orchestrator](https://github.com/meridianmindx/meridian-crewai-deploy-orchestrator)
Deploy CrewAI agents anywhere with one command. Automatically analyze agent codebases and generate optimized Docker configurations for cloud deployment.

**Perfect companion for MCP deployments:** Deploy your CrewAI agents alongside MCP servers using the same unified approach.

### 🔄 [Meridian Context Compression](https://github.com/meridianmindx/meridian-context-compression)
Reduce LLM token usage by 22x while preserving semantic meaning. Cut your OpenAI and Anthropic API costs dramatically with intelligent context compression.

**Works great with MCP:** Compress prompts before sending to expensive LLMs, especially useful when MCP servers retrieve large documents.

### 📦 Installation Bundle

```bash
# Install the complete Meridian tooling suite
pip install meridian-mcp-deploy meridian-context-compression
# Or individually
pip install meridian-crewai-deploy-orchestrator
```

### 🎯 Why Use All Three?

1. **meridian-mcp-deploy**: Containerize and deploy your MCP servers
2. **meridian-crewai-deploy-orchestrator**: Deploy your CrewAI agents
3. **meridian-context-compression**: Optimize token usage for both

**Together, they provide a complete AI agent deployment and optimization stack.**

---

<div align="center">

## ⭐ Support This Project

**If meridian-mcp-deploy saves you time, please consider starring it on GitHub!**

[![Star us on GitHub](https://img.shields.io/badge/-⭐_Star_this_repo-black?style=for-the-badge&logo=github)](https://github.com/meridianmindx/meridian-mcp-deploy/stargazers)

*Stars help other developers discover useful tools in the growing MCP ecosystem.*

</div>
