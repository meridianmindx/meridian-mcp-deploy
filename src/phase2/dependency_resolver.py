#!/usr/bin/env python3
"""
Dependency Resolution Script for MCP Deployment Framework

Analyzes Python imports in source files and maps them to apt packages.
Helps identify system-level dependencies needed for MCP server deployment.
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, Set, List, Optional


# Mapping of common Python modules to their apt package names
MODULE_TO_APT_MAP = {
    'yaml': 'python3-yaml',
    'requests': 'python3-requests',
    'urllib3': 'python3-urllib3',
    'certifi': 'python3-certifi',
    'flask': 'python3-flask',
    'django': 'python3-django',
    'fastapi': 'python3-fastapi',
    'uvicorn': 'python3-uvicorn',
    'psycopg2': 'python3-psycopg2',
    'pymysql': 'python3-pymysql',
    'redis': 'python3-redis',
    'pymongo': 'python3-pymongo',
    'numpy': 'python3-numpy',
    'pandas': 'python3-pandas',
    'aiohttp': 'python3-aiohttp',
    'httpx': 'python3-httpx',
    'cryptography': 'python3-cryptography',
    'psutil': 'python3-psutil',
    'pytest': 'python3-pytest',
    'loguru': 'python3-loguru',
    'dotenv': 'python3-dotenv',
    'click': 'python3-click',
    'typer': 'python3-typer',
}

# Modules that are part of Python standard library
STDLIB_MODULES = {
    'os', 'sys', 'pathlib', 'typing', 're', 'json', 'csv', 'datetime',
    'time', 'random', 'math', 'string', 'collections', 'itertools',
    'functools', 'operator', 'argparse', 'configparser', 'subprocess',
    'socket', 'ssl', 'asyncio', 'logging', 'hashlib', 'struct', 'io',
    'tempfile', 'shutil', 'glob', 'fnmatch', 'stat', 'copy', 'pprint',
    'enum', 'dataclasses', 'contextlib', 'abc', 'warnings', 'traceback',
    'unittest', 'threading', 'multiprocessing', 'concurrent', 'queue',
    'html', 'xml', 'email', 'http', 'urllib', 'base64', 'binascii',
    'zlib', 'gzip', 'bz2', 'zipfile', 'tarfile', 'pickle', 'marshal',
    'sqlite3', 'uuid', 'secrets', 'secrets', 'textwrap', 'difflib',
}


class DependencyResolver:
    """Resolve Python dependencies to system packages"""
    
    def __init__(self):
        self.import_map = MODULE_TO_APT_MAP.copy()
        self.stdlib = STDLIB_MODULES.copy()
    
    def extract_imports(self, file_path: str) -> Set[str]:
        """Extract all imports from a Python file using AST"""
        imports = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name.split('.')[0]
                        imports.add(module_name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module_name = node.module.split('.')[0]
                        imports.add(module_name)
        
        except SyntaxError as e:
            print(f"Warning: Syntax error in {file_path}: {e}")
        except Exception as e:
            print(f"Warning: Error reading {file_path}: {e}")
        
        return imports
    
    def scan_directory(self, directory: str, pattern: str = "*.py") -> Dict[str, Set[str]]:
        """Scan a directory for Python files and extract imports"""
        file_imports = {}
        dir_path = Path(directory)
        
        for py_file in dir_path.rglob(pattern):
            if 'venv' not in str(py_file) and '__pycache__' not in str(py_file):
                rel_path = str(py_file.relative_to(dir_path))
                imports = self.extract_imports(str(py_file))
                if imports:
                    file_imports[rel_path] = imports
        
        return file_imports
    
    def generate_requirements(self, file_imports: Dict[str, Set[str]]) -> Dict[str, List[str]]:
        """Categorize imports into apt packages and pip requirements"""
        apt_packages = set()
        pip_packages = set()
        stdlib_imports = set()
        
        all_imports = set()
        for imports in file_imports.values():
            all_imports.update(imports)
        
        for module in all_imports:
            if module in self.stdlib:
                stdlib_imports.add(module)
            elif module in self.import_map:
                apt_packages.add(self.import_map[module])
            else:
                pip_packages.add(module)
        
        return {
            'apt': sorted(apt_packages),
            'pip': sorted(pip_packages),
            'stdlib': sorted(stdlib_imports)
        }
    
    def generate_install_script(self, apt_packages: List[str], pip_packages: List[str]) -> str:
        """Generate a bash installation script"""
        script = """#!/bin/bash
# Auto-generated dependency installation script
set -e

echo "Installing system dependencies..."
"""
        if apt_packages:
            script += f"apt-get update && apt-get install -y {' '.join(apt_packages)}\n"
        else:
            script += 'echo "No apt packages to install"\n'
        
        script += '\necho "Installing Python dependencies..."\n'
        
        if pip_packages:
            script += f"pip3 install {' '.join(pip_packages)}\n"
        else:
            script += 'echo "No pip packages to install"\n'
        
        script += '\necho "Dependency installation complete!"\n'
        return script
    
    def add_mapping(self, module: str, apt_package: str):
        """Add a custom mapping from module to apt package"""
        self.import_map[module] = apt_package


def main():
    """Main entry point for CLI usage"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(
        description='Resolve Python imports to apt packages'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to scan for Python files (default: current directory)'
    )
    parser.add_argument(
        '-o', '--output',
        choices=['text', 'json', 'script'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--script-output',
        default='install_deps.sh',
        help='Output path for installation script (default: install_deps.sh)'
    )
    
    args = parser.parse_args()
    
    resolver = DependencyResolver()
    
    print(f"Scanning directory: {args.directory}")
    file_imports = resolver.scan_directory(args.directory)
    
    if not file_imports:
        print("No Python files found or no imports detected.")
        return 0
    
    all_imports = set()
    for imports in file_imports.values():
        all_imports.update(imports)
    
    print(f"\nFound {len(file_imports)} Python files with imports")
    print(f"Total unique imports: {len(all_imports)}")
    
    categories = resolver.generate_requirements(file_imports)
    
    if args.output == 'text':
        print("\n=== Dependency Analysis ===\n")
        
        print("APT Packages:")
        if categories['apt']:
            for pkg in categories['apt']:
                print(f"  - {pkg}")
        else:
            print("  (none)")
        
        print(f"\nPIP Packages:")
        if categories['pip']:
            for pkg in categories['pip']:
                print(f"  - {pkg}")
        else:
            print("  (none)")
        
        print(f"\nStandard Library: {len(categories['stdlib'])} modules")
        
    elif args.output == 'json':
        print(json.dumps(categories, indent=2))
        
    elif args.output == 'script':
        script = resolver.generate_install_script(
            categories['apt'],
            categories['pip']
        )
        with open(args.script_output, 'w') as f:
            f.write(script)
        os.chmod(args.script_output, 0o755)
        print(f"\nInstallation script written to: {args.script_output}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
