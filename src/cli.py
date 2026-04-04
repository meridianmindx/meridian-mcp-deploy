"""Command Line Interface for MCP Deployment Framework"""

import argparse
import sys
import os
from pathlib import Path
from typing import List

from manifest_parser import ManifestParser
from docker_compose_generator import DockerComposeGenerator
from health_check import HealthCheckSystem


class MCPDeployCLI:
    """Main CLI for MCP Deployment Framework"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description='MCP Server Deployment Framework',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Commands')
        
        # Validate command
        validate_parser = subparsers.add_parser('validate', help='Validate manifest file')
        validate_parser.add_argument('manifest', help='Path to manifest YAML file')
        
        # Generate command
        generate_parser = subparsers.add_parser('generate', help='Generate Docker Compose configuration')
        generate_parser.add_argument('manifests', nargs='+', help='Paths to manifest YAML files')
        generate_parser.add_argument('-o', '--output', default='docker-compose.yml', 
                                    help='Output file path (default: docker-compose.yml)')
        
        # Health check command
        health_parser = subparsers.add_parser('health', help='Perform health check')
        health_parser.add_argument('manifest', help='Path to manifest YAML file')
        health_parser.add_argument('--retries', type=int, default=None, 
                                  help='Number of retries (default: from manifest)')
        
        # List command
        list_parser = subparsers.add_parser('list', help='List parsed manifests')
        list_parser.add_argument('manifests', nargs='+', help='Paths to manifest YAML files')
        
        return parser
    
    def run(self, args: List[str] = None):
        """Run the CLI with given arguments"""
        if args is None:
            args = sys.argv[1:]
        
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return 1
        
        try:
            if parsed_args.command == 'validate':
                return self._validate_command(parsed_args)
            elif parsed_args.command == 'generate':
                return self._generate_command(parsed_args)
            elif parsed_args.command == 'health':
                return self._health_command(parsed_args)
            elif parsed_args.command == 'list':
                return self._list_command(parsed_args)
        except Exception as e:
            print(f"Error: {e}")
            return 1
        
        return 0
    
    def _validate_command(self, args):
        """Handle validate command"""
        try:
            manifest = ManifestParser.parse_file(args.manifest)
            manifest.validate()
            print(f"✓ Manifest '{manifest.name}' v{manifest.version} is valid")
            print(f"  Runtime: {manifest.runtime.value}")
            if manifest.description:
                print(f"  Description: {manifest.description}")
            return 0
        except Exception as e:
            print(f"✗ Validation failed: {e}")
            return 1
    
    def _generate_command(self, args):
        """Handle generate command"""
        manifests = []
        for manifest_path in args.manifests:
            try:
                manifest = ManifestParser.parse_file(manifest_path)
                manifests.append(manifest)
                print(f"✓ Parsed manifest: {manifest.name}")
            except Exception as e:
                print(f"✗ Failed to parse {manifest_path}: {e}")
                return 1
        
        if not manifests:
            print("No valid manifests to generate from")
            return 1
        
        try:
            compose_config = DockerComposeGenerator.generate_from_manifests(manifests)
            DockerComposeGenerator.write_compose_file(compose_config, args.output)
            print(f"✓ Generated Docker Compose configuration: {args.output}")
            print(f"  Services: {', '.join(compose_config['services'].keys())}")
            return 0
        except Exception as e:
            print(f"✗ Generation failed: {e}")
            return 1
    
    def _health_command(self, args):
        """Handle health check command"""
        try:
            manifest = ManifestParser.parse_file(args.manifest)
            
            if not manifest.health_check:
                print(f"✗ No health check configured for {manifest.name}")
                return 1
            
            print(f"Performing health check for {manifest.name}...")
            success, message = HealthCheckSystem.check_with_retry(
                manifest.health_check,
                max_retries=args.retries
            )
            
            if success:
                print(f"✓ Health check passed: {message}")
                return 0
            else:
                print(f"✗ Health check failed: {message}")
                return 1
                
        except Exception as e:
            print(f"✗ Health check error: {e}")
            return 1
    
    def _list_command(self, args):
        """Handle list command"""
        for manifest_path in args.manifests:
            try:
                manifest = ManifestParser.parse_file(manifest_path)
                print(f"\n{manifest.name} (v{manifest.version}):")
                print(f"  Runtime: {manifest.runtime.value}")
                print(f"  Port: {manifest.port or 'N/A'}")
                print(f"  Health Check: {'Yes' if manifest.health_check else 'No'}")
                if manifest.description:
                    print(f"  Description: {manifest.description[:60]}...")
            except Exception as e:
                print(f"✗ Failed to parse {manifest_path}: {e}")
        
        return 0


def main():
    """Main entry point"""
    cli = MCPDeployCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()
