"""YAML Manifest Parser for MCP Servers"""

import yaml
from typing import Dict, Any
from manifest_schema import MCPManifest, RuntimeType, HealthCheck, HealthCheckType, VolumeMount, EnvironmentVariable


class ManifestParser:
    """Parse and validate MCP server manifests from YAML"""
    
    @staticmethod
    def parse_yaml(yaml_content: str) -> MCPManifest:
        """Parse YAML content into MCPManifest object"""
        data = yaml.safe_load(yaml_content)
        return ManifestParser._parse_dict(data)
    
    @staticmethod
    def parse_file(file_path: str) -> MCPManifest:
        """Parse YAML file into MCPManifest object"""
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return ManifestParser._parse_dict(data)
    
    @staticmethod
    def _parse_dict(data: Dict[str, Any]) -> MCPManifest:
        """Parse dictionary into MCPManifest"""
        
        # Validate required fields exist
        required_fields = ['name', 'version', 'runtime']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # Parse runtime
        try:
            runtime = RuntimeType(data['runtime'].lower())
        except ValueError:
            raise ValueError(f"Invalid runtime type: {data['runtime']}. Must be one of: {[rt.value for rt in RuntimeType]}")
        
        # Parse health check if present
        health_check = None
        if 'health_check' in data:
            hc_data = data['health_check']
            hc_type = HealthCheckType(hc_data.get('type', 'tcp').lower())
            health_check = HealthCheck(
                type=hc_type,
                endpoint=hc_data.get('endpoint'),
                command=hc_data.get('command'),
                timeout_seconds=hc_data.get('timeout_seconds', 30),
                interval_seconds=hc_data.get('interval_seconds', 60),
                retries=hc_data.get('retries', 3)
            )
        
        # Parse volumes if present
        volumes = None
        if 'volumes' in data:
            volumes = []
            for vol_data in data['volumes']:
                volumes.append(VolumeMount(
                    source=vol_data['source'],
                    target=vol_data['target'],
                    read_only=vol_data.get('read_only', False)
                ))
        
        # Parse environment variables if present
        environment = None
        if 'environment' in data:
            environment = []
            for env_data in data['environment']:
                environment.append(EnvironmentVariable(
                    name=env_data['name'],
                    value=env_data['value'],
                    secret=env_data.get('secret', False)
                ))
        
        # Create manifest object
        manifest = MCPManifest(
            name=data['name'],
            version=data['version'],
            runtime=runtime,
            docker_image=data.get('docker_image'),
            entrypoint=data.get('entrypoint'),
            command=data.get('command'),
            port=data.get('port'),
            host=data.get('host', 'localhost'),
            memory_limit=data.get('memory_limit'),
            cpu_shares=data.get('cpu_shares'),
            volumes=volumes,
            environment=environment,
            health_check=health_check,
            description=data.get('description'),
            maintainer=data.get('maintainer'),
            license=data.get('license')
        )
        
        # Validate the manifest
        manifest.validate()
        
        return manifest
    
    @staticmethod
    def validate_schema(yaml_content: str) -> bool:
        """Validate YAML against schema without creating objects"""
        try:
            ManifestParser.parse_yaml(yaml_content)
            return True
        except Exception as e:
            print(f"Schema validation failed: {e}")
            return False
