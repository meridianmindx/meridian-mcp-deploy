"""Health Check System for MCP Servers"""

import subprocess
import socket
import time
from typing import Optional, Tuple
from manifest_schema import HealthCheck, HealthCheckType


class HealthCheckSystem:
    """Perform health checks on MCP servers"""
    
    @staticmethod
    def check_tcp(endpoint: str, timeout: int = 30) -> Tuple[bool, str]:
        """Check TCP connectivity"""
        try:
            if ':' in endpoint:
                host, port_str = endpoint.split(':')
                port = int(port_str)
            else:
                host = 'localhost'
                port = int(endpoint)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                if result == 0:
                    return True, f"TCP connection successful to {host}:{port}"
                else:
                    return False, f"TCP connection failed to {host}:{port} (error: {result})"
        except Exception as e:
            return False, f"TCP check error: {str(e)}"
    
    @staticmethod
    def check_http(endpoint: str, timeout: int = 30) -> Tuple[bool, str]:
        """Check HTTP endpoint"""
        try:
            import requests
            response = requests.get(endpoint, timeout=timeout)
            if response.status_code < 400:
                return True, f"HTTP check successful: {response.status_code}"
            else:
                return False, f"HTTP check failed: {response.status_code}"
        except ImportError:
            # Fallback to curl if requests is not available
            try:
                cmd = ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', endpoint, '--max-time', str(timeout)]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.isdigit():
                    status_code = int(result.stdout)
                    if status_code < 400:
                        return True, f"HTTP check successful: {status_code}"
                    else:
                        return False, f"HTTP check failed: {status_code}"
                else:
                    return False, f"HTTP check failed: {result.stderr}"
            except Exception as e:
                return False, f"HTTP check error: {str(e)}"
        except Exception as e:
            return False, f"HTTP check error: {str(e)}"
    
    @staticmethod
    def check_command(command: str, timeout: int = 30) -> Tuple[bool, str]:
        """Check command execution"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                timeout=timeout,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return True, f"Command check successful: {result.stdout[:100]}..."
            else:
                return False, f"Command check failed (exit code {result.returncode}): {result.stderr}"
        except subprocess.TimeoutExpired:
            return False, f"Command check timeout after {timeout} seconds"
        except Exception as e:
            return False, f"Command check error: {str(e)}"
    
    @staticmethod
    def perform_health_check(health_check: HealthCheck) -> Tuple[bool, str]:
        """Perform health check based on configuration"""
        if health_check.type == HealthCheckType.TCP:
            return HealthCheckSystem.check_tcp(
                health_check.endpoint,
                timeout=health_check.timeout_seconds
            )
        elif health_check.type == HealthCheckType.HTTP:
            return HealthCheckSystem.check_http(
                health_check.endpoint,
                timeout=health_check.timeout_seconds
            )
        elif health_check.type == HealthCheckType.COMMAND:
            return HealthCheckSystem.check_command(
                health_check.command,
                timeout=health_check.timeout_seconds
            )
        else:
            return False, f"Unknown health check type: {health_check.type}"
    
    @staticmethod
    def check_with_retry(health_check: HealthCheck, max_retries: Optional[int] = None) -> Tuple[bool, str]:
        """Perform health check with retries"""
        retries = max_retries or health_check.retries
        
        for attempt in range(retries):
            success, message = HealthCheckSystem.perform_health_check(health_check)
            if success:
                return True, f"Success on attempt {attempt + 1}: {message}"
            
            if attempt < retries - 1:
                time.sleep(health_check.interval_seconds)
        
        return False, f"Failed after {retries} attempts: {message}"
