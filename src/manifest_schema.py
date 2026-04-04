"""MCP Server Manifest Schema Definition"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class RuntimeType(str, Enum):
    """Supported runtime types for MCP servers"""
    DOCKER = "docker"
    NODE = "node"
    PYTHON = "python"
    BINARY = "binary"


class HealthCheckType(str, Enum):
    """Types of health checks"""
    TCP = "tcp"
    HTTP = "http"
    COMMAND = "command"


@dataclass
class HealthCheck:
    """Health check configuration"""
    type: HealthCheckType
    endpoint: Optional[str] = None  # For HTTP/TCP checks
    command: Optional[str] = None  # For command checks
    timeout_seconds: int = 30
    interval_seconds: int = 60
    retries: int = 3


@dataclass
class VolumeMount:
    """Docker volume mount configuration"""
    source: str
    target: str
    read_only: bool = False


@dataclass
class EnvironmentVariable:
    """Environment variable configuration"""
    name: str
    value: str
    secret: bool = False


@dataclass
class MCPManifest:
    """MCP Server Manifest"""
    # Required fields
    name: str
    version: str
    runtime: RuntimeType
    
    # Runtime-specific configuration
    docker_image: Optional[str] = None
    entrypoint: Optional[str] = None
    command: Optional[Union[str, List[str]]] = None
    
    # Networking
    port: Optional[int] = None
    host: str = "localhost"
    
    # Resource constraints
    memory_limit: Optional[str] = None  # e.g., "512m", "1g"
    cpu_shares: Optional[int] = None
    
    # Volumes
    volumes: Optional[List[VolumeMount]] = None
    
    # Environment
    environment: Optional[List[EnvironmentVariable]] = None
    
    # Health checks
    health_check: Optional[HealthCheck] = None
    
    # Metadata
    description: Optional[str] = None
    maintainer: Optional[str] = None
    license: Optional[str] = None
    
    def validate(self):
        """Validate the manifest"""
        if not self.name:
            raise ValueError("Manifest must have a name")
        if not self.version:
            raise ValueError("Manifest must have a version")
        if not self.runtime:
            raise ValueError("Manifest must specify a runtime type")
        
        # Runtime-specific validation
        if self.runtime == RuntimeType.DOCKER and not self.docker_image:
            raise ValueError("Docker runtime requires docker_image field")
        
        # Health check validation
        if self.health_check:
            if self.health_check.type == HealthCheckType.HTTP and not self.health_check.endpoint:
                raise ValueError("HTTP health check requires an endpoint")
            if self.health_check.type == HealthCheckType.TCP and not self.health_check.endpoint:
                raise ValueError("TCP health check requires an endpoint")
            if self.health_check.type == HealthCheckType.COMMAND and not self.health_check.command:
                raise ValueError("Command health check requires a command")
