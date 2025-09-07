#!/usr/bin/env python3
"""
Enhanced API Test Agent with Bearer Token Support
Supports both query parameter and Bearer token authentication methods.
"""

import sys
import os
from pathlib import Path
from agent.utils import load_swagger, ensure_dirs, get_paths
from agent.generator import generate_tests, extract_curl_commands
from agent.bearer_auth_generator import generate_bearer_auth_tests, generate_curl_commands_bearer, detect_auth_method
from agent.runner import run_tests

def main():
    if len(sys.argv) < 2:
        print("Usage: python enhanced_main.py <api_name> [--auth-method <method>]")
        print("Auth methods: auto, query_param, bearer_token")
        print("Example: python enhanced_main.py empdetails --auth-method bearer_token")
        sys.exit(1)

    api_name = sys.argv[1]
    auth_method = "auto"  # default
    
    # Parse command line arguments
    if len(sys.argv) > 2 and sys.argv[2] == "--auth-method":
        if len(sys.argv) > 3:
            auth_method = sys.argv[3]
        else:
            print("Error: --auth-method requires a value")
            sys.exit(1)

    print(f"[INFO] Running enhanced agent for API: {api_name}")
    print(f"[INFO] Authentication method: {auth_method}")

    # Prepare directories
    ensure_dirs(api_name)
    paths = get_paths(api_name)

    # Load swagger spec
    schema = load_swagger(api_name)

    # Detect authentication method if auto
    if auth_method == "auto":
        detected_method = detect_auth_method(schema)
        print(f"[INFO] Auto-detected authentication method: {detected_method}")
        auth_method = detected_method

    # Generate tests based on authentication method
    if auth_method == "bearer_token":
        print("[INFO] Generating tests with Bearer token authentication")
        test_code = generate_bearer_auth_tests(api_name, schema)
        curl_commands = generate_curl_commands_bearer(schema)
    else:
        print("[INFO] Generating tests with query parameter authentication")
        test_code = generate_tests(api_name, schema)
        curl_commands = extract_curl_commands(test_code)

    # Write test file
    with open(paths["test_file"], "w") as f:
        f.write(test_code)
    print(f"[INFO] Test file created: {paths['test_file']}")

    # Write curl commands file
    curl_file = f"curl_commands_{api_name}.txt"
    with open(curl_file, "w") as f:
        f.write(f"# Curl commands for {api_name} API testing\n")
        f.write(f"# Authentication method: {auth_method}\n")
        f.write(f"# Base URL: {schema.get('servers', [{}])[0].get('url', 'https://merp.intermesh.net')}\n\n")
        f.write(curl_commands)
    print(f"[INFO] Curl commands file created: {curl_file}")

    # Run tests
    run_tests(paths["test_file"], paths["result_file"])

def show_auth_methods():
    """Show available authentication methods and their descriptions."""
    methods = {
        "auto": "Automatically detect authentication method from Swagger spec",
        "query_param": "Use query parameters for authentication (e.g., ?AK=token)",
        "bearer_token": "Use Bearer token in Authorization header"
    }
    
    print("Available Authentication Methods:")
    print("=" * 50)
    for method, description in methods.items():
        print(f"{method:15} - {description}")
    print()

def show_examples():
    """Show usage examples."""
    print("Usage Examples:")
    print("=" * 30)
    print("# Auto-detect authentication method")
    print("python enhanced_main.py empdetails")
    print()
    print("# Force Bearer token authentication")
    print("python enhanced_main.py empdetails --auth-method bearer_token")
    print()
    print("# Force query parameter authentication")
    print("python enhanced_main.py empdetails --auth-method query_param")
    print()

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] in ["--help", "-h"]:
        print("Enhanced API Test Agent with Bearer Token Support")
        print("=" * 50)
        show_auth_methods()
        show_examples()
        sys.exit(0)
    
    main()
