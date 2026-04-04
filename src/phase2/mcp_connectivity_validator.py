#!/usr/bin/env python3
"""
MCP Server Connectivity Validator

Tests connectivity to MCP servers using various protocols.
Supports HTTP, TCP, and stdio-based MCP server connections.
"""

import socket
import subprocess
import time
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ConnectionType(Enum):
    HTTP = "http"
    TCP = "tcp"
    STDIO = "stdio"
    SSE = "sse"


@dataclass
class ConnectionResult:
    server_name: str
    connection_type: str
    success: bool
    response_time_ms: float
    message: str
    details: Optional[dict] = None


class MCPConnectivityValidator:
    """Validate connectivity to MCP servers"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
    
    def check_http(self, url: str) -> Tuple[bool, str, float]:
        """Check HTTP/HTTPS endpoint availability"""
        start_time = time.time()
        
        try:
            import requests
            response = requests.get(url, timeout=self.timeout)
            elapsed = (time.time() - start_time) * 1000
            
            if response.status_code < 400:
                return True, f"HTTP {response.status_code}", elapsed
            else:
                return False, f"HTTP {response.status_code}", elapsed
                
        except ImportError:
            # Fallback to curl
            try:
                cmd = ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code} %{time_total}', 
                       url, '--max-time', str(self.timeout)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
                elapsed = (time.time() - start_time) * 1000
                
                if result.returncode == 0:
                    parts = result.stdout.strip().split()
                    if len(parts) >= 2:
                        status = parts[0]
                        if status.isdigit() and int(status) < 400:
                            return True, f"HTTP {status}", elapsed
                return False, "HTTP check failed", elapsed
            except Exception as e:
                return False, str(e), (time.time() - start_time) * 1000
                
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            return False, str(e), elapsed
    
    def check_tcp(self, host: str, port: int) -> Tuple[bool, str, float]:
        """Check TCP port availability"""
        start_time = time.time()
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((host, port))
                elapsed = (time.time() - start_time) * 1000
                
                if result == 0:
                    return True, "TCP connection successful", elapsed
                else:
                    return False, f"TCP connection failed (error: {result})", elapsed
                    
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            return False, str(e), elapsed
    
    def check_stdio(self, command: List[str], test_input: str = None) -> Tuple[bool, str, float]:
        """Check stdio-based MCP server startup"""
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                process.wait(timeout=min(self.timeout, 5))
                
                if process.returncode == 0:
                    elapsed = (time.time() - start_time) * 1000
                    return True, "Command executed successfully", elapsed
                else:
                    elapsed = (time.time() - start_time) * 1000
                    return False, f"Command failed with code {process.returncode}", elapsed
                    
            except subprocess.TimeoutExpired:
                process.kill()
                elapsed = (time.time() - start_time) * 1000
                return True, "Process started (timeout reached, likely running)", elapsed
                
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            return False, str(e), elapsed
    
    def check_mcp_initialization(self, command: List[str]) -> Tuple[bool, str, float, Optional[dict]]:
        """
        Test MCP server initialization via stdio
        Sends initialize request and waits for response
        """
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Send initialize request
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "mcp-validator", "version": "1.0.0"}
                }
            }
            
            process.stdin.write(json.dumps(init_request) + '\n')
            process.stdin.flush()
            
            # Wait for response with timeout
            start_wait = time.time()
            response = None
            
            while time.time() - start_wait < self.timeout:
                if process.stdout.readline:
                    line = process.stdout.readline().strip()
                    if line:
                        try:
                            response = json.loads(line)
                            break
                        except:
                            continue
            
            process.terminate()
            elapsed = (time.time() - start_time) * 1000
            
            if response:
                if 'result' in response:
                    return True, "MCP initialization successful", elapsed, response.get('result')
                elif 'error' in response:
                    return False, f"MCP error: {response['error']}", elapsed, response['error']
            
            return False, "No valid MCP response", elapsed, None
            
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            return False, str(e), elapsed, None
    
    def validate_server(self, config: dict) -> ConnectionResult:
        """Validate a single server configuration"""
        name = config.get('name', 'unknown')
        conn_type = config.get('type', 'tcp')
        
        if conn_type == 'http':
            url = config.get('url', '')
            success, message, elapsed = self.check_http(url)
            
        elif conn_type == 'tcp':
            host = config.get('host', 'localhost')
            port = config.get('port', 0)
            success, message, elapsed = self.check_tcp(host, port)
            
        elif conn_type == 'stdio':
            command = config.get('command', [])
            success, message, elapsed = self.check_stdio(command)
            
        else:
            success, message, elapsed = False, f"Unknown connection type: {conn_type}", 0
        
        return ConnectionResult(
            server_name=name,
            connection_type=conn_type,
            success=success,
            response_time_ms=elapsed,
            message=message
        )
    
    def validate_multiple(self, configs: List[dict]) -> List[ConnectionResult]:
        """Validate multiple server configurations"""
        results = []
        for config in configs:
            result = self.validate_server(config)
            results.append(result)
        return results
    
    def generate_report(self, results: List[ConnectionResult]) -> str:
        """Generate a text report from validation results"""
        lines = []
        lines.append("\n=== MCP Connectivity Validation Report ===\n")
        
        total = len(results)
        successful = sum(1 for r in results if r.success)
        
        for result in results:
            status = "✓" if result.success else "✗"
            lines.append(f"{status} {result.server_name} ({result.connection_type})")
            lines.append(f"    Status: {result.message}")
            lines.append(f"    Response time: {result.response_time_ms:.2f}ms")
            lines.append("")
        
        lines.append(f"Summary: {successful}/{total} servers reachable")
        
        return '\n'.join(lines)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate MCP server connectivity'
    )
    parser.add_argument(
        '--config', '-c',
        help='JSON config file with server definitions'
    )
    parser.add_argument(
        '--http',
        help='Test HTTP endpoint (URL)'
    )
    parser.add_argument(
        '--tcp',
        help='Test TCP endpoint (host:port)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Timeout in seconds (default: 30)'
    )
    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    args = parser.parse_args()
    
    validator = MCPConnectivityValidator(timeout=args.timeout)
    results = []
    
    if args.config:
        with open(args.config, 'r') as f:
            configs = json.load(f)
        
        if isinstance(configs, dict):
            configs = [configs]
        
        results = validator.validate_multiple(configs)
        
    elif args.http:
        success, message, elapsed = validator.check_http(args.http)
        results.append(ConnectionResult(
            server_name=args.http,
            connection_type='http',
            success=success,
            response_time_ms=elapsed,
            message=message
        ))
        
    elif args.tcp:
        if ':' in args.tcp:
            host, port = args.tcp.rsplit(':', 1)
            port = int(port)
        else:
            host = 'localhost'
            port = int(args.tcp)
        
        success, message, elapsed = validator.check_tcp(host, port)
        results.append(ConnectionResult(
            server_name=f"{host}:{port}",
            connection_type='tcp',
            success=success,
            response_time_ms=elapsed,
            message=message
        ))
    else:
        parser.print_help()
        return 1
    
    # Output results
    if args.output == 'json':
        output = []
        for r in results:
            output.append({
                'server': r.server_name,
                'type': r.connection_type,
                'success': r.success,
                'message': r.message,
                'response_time_ms': r.response_time_ms
            })
        print(json.dumps(output, indent=2))
    else:
        print(validator.generate_report(results))
    
    # Return success only if all checks passed
    return 0 if all(r.success for r in results) else 1


if __name__ == '__main__':
    sys.exit(main())
