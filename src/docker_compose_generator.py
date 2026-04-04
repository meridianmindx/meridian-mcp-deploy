"""Docker Compose Generator for MCP Servers"""

import yaml
from typing import Dict, Any, List
from manifest_schema import MCPManifest, RuntimeType


class DockerComposeGenerator:
    """Generate Docker Compose configuration from MCP manifests"""
    
    @staticmethod
    def generate_single(manifest: MCPManifest) -> Dict[str, Any]:
        """Generate Docker Compose configuration for a single MCP server"""
        if manifest.runtime != RuntimeType.DOCKER:
            raise ValueError(f"Cannot generate Docker Compose for runtime type: {manifest.runtime}")
        
        service_name = manifest.name.replace('_', '-').lower()
        
        # Build service configuration
        service_config = {
            'image': manifest.docker_image,
            'container_name': f"mcp-{service_name}",
        }
        
        # Add entrypoint if specified
        if manifest.entrypoint:
            service_config['entrypoint'] = manifest.entrypoint
        
        # Add command if specified
        if manifest.command:
            if isinstance(manifest.command, list):
                service_config['command'] = manifest.command
            else:
                service_config['command'] = manifest.command
        
        # Add ports if specified
        if manifest.port:
            service_config['ports'] = [f"{manifest.port}:{manifest.port}"]
        
        # Add volumes if specified
        if manifest.volumes:
            service_config['volumes'] = []
            for volume in manifest.volumes:
                if volume.read_only:
                    service_config['volumes'].append(f"{volume.source}:{volume.target}:ro")
                else:
                    service_config['volumes'].append(f"{volume.source}:{volume.target}")
        
        # Add environment variables if specified
        if manifest.environment:
            service_config['environment'] = {}
            for env_var in manifest.environment:
                service_config['environment'][env_var.name] = env_var.value
        
        # Add resource constraints if specified
        if manifest.memory_limit:
            service_config['deploy'] = {
                'resources': {
                    'limits': {
                        'memory': manifest.memory_limit
                    }
                }
            }
        
        # Add health check if specified
        if manifest.health_check:
            health_check_config = DockerComposeGenerator._build_health_check(manifest.health_check)
            if health_check_config:
                service_config['healthcheck'] = health_check_config
        
        return {service_name: service_config}
    
    @staticmethod
    def _build_health_check(health_check) -> Dict[str, Any]:
        """Build Docker Compose health check configuration"""
        if health_check.type.value == 'command':
            return {
                'test': health_check.command,
                'interval': f"{health_check.interval_seconds}s",
                'timeout': f"{health_check.timeout_seconds}s",
                'retries': health_check.retries
            }
        elif health_check.type.value == 'http':
            return {
                'test': f"curl -f {health_check.endpoint} || exit 1",
                'interval': f"{health_check.interval_seconds}s",
                'timeout': f"{health_check.timeout_seconds}s",
                'retries': health_check.retries
            }
        elif health_check.type.value == 'tcp':
            # Extract host and port from endpoint
            if ':' in health_check.endpoint:
                host, port = health_check.endpoint.split(':')
            else:
                host = 'localhost'
                port = health_check.endpoint
            
            return {
                'test': f"nc -z {host} {port}",
                'interval': f"{health_check.interval_seconds}s",
                'timeout': f"{health_check.timeout_seconds}s",
                'retries': health_check.retries
            }
        return None
    
    @staticmethod
    def generate_from_manifests(manifests: List[MCPManifest]) -> Dict[str, Any]:
        """Generate Docker Compose configuration from multiple manifests"""
        compose_config = {
            'version': '3.8',
            'services': {}
        }
        
        for manifest in manifests:
            if manifest.runtime == RuntimeType.DOCKER:
                service_config = DockerComposeGenerator.generate_single(manifest)
                compose_config['services'].update(service_config)
        
        return compose_config
    
    @staticmethod
    def write_compose_file(compose_config: Dict[str, Any], output_path: str):
        """Write Docker Compose configuration to YAML file"""
        with open(output_path, 'w') as f:
            yaml.dump(compose_config, f, default_flow_style=False, sort_keys=False)
