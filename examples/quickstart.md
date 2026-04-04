# Quick Start Guide

## Installation

### From PyPI (recommended)

```bash
pip install mcp-deploy
```

### From source

```bash
git clone https://github.com/meridian/mcp-deploy.git
cd mcp-deploy-framework
pip install -r requirements.txt
```

## Basic Usage

### 1. Validate a manifest

```bash
mcp-deploy validate manifests/filesystem-server.yaml
```

Output:
```
✓ Manifest 'filesystem-server' v1.0.0 is valid
 Runtime: docker
 Description: MCP filesystem server for file operations
```

### 2. Generate Docker Compose configuration

```bash
mcp-deploy generate manifests/filesystem-server.yaml -o docker-compose.yml
```

### 3. Deploy with Docker Compose

```bash
docker-compose up -d
```

## Next Steps

- See `examples/README.md` for more example manifests
- Read the main `README.md` for full documentation
- Create your own manifest by copying an example

## Troubleshooting

If you encounter issues:

1. Ensure Python 3.9+ is installed
2. Check that `pyyaml` and `requests` are installed: `pip install -r requirements.txt`
3. Validate your manifest syntax with `mcp-deploy validate`
