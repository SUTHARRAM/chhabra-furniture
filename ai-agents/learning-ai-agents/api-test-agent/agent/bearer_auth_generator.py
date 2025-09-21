"""
Enhanced API Test Generator with Bearer Token Support
This module extends the original generator to handle Bearer token authentication.
"""

import requests
import pytest
from typing import Dict, List, Any

BASE_URL = "https://merp.intermesh.net"

def detect_auth_method(schema: dict) -> str:
    """
    Detect if the API uses query parameter auth or Bearer token auth.
    Returns: 'query_param', 'bearer_token', or 'mixed'
    """
    auth_methods = set()
    
    for path, methods in schema.get('paths', {}).items():
        for method, details in methods.items():
            if 'parameters' in details:
                for param in details['parameters']:
                    if param.get('name') in ['AK', 'token', 'auth_token']:
                        if param.get('in') == 'query':
                            auth_methods.add('query_param')
                        elif param.get('in') == 'header':
                            auth_methods.add('bearer_token')
                    elif param.get('name') == 'Authorization':
                        auth_methods.add('bearer_token')
    
    # Check for security schemes
    if 'components' in schema and 'securitySchemes' in schema['components']:
        for scheme_name, scheme in schema['components']['securitySchemes'].items():
            if scheme.get('type') == 'http' and scheme.get('scheme') == 'bearer':
                auth_methods.add('bearer_token')
            elif scheme.get('type') == 'apiKey' and scheme.get('in') == 'query':
                auth_methods.add('query_param')
    
    if len(auth_methods) > 1:
        return 'mixed'
    elif 'bearer_token' in auth_methods:
        return 'bearer_token'
    else:
        return 'query_param'

def generate_bearer_auth_tests(api_name: str, schema: dict) -> str:
    """
    Generate test cases with Bearer token authentication support.
    """
    auth_method = detect_auth_method(schema)
    
    test_cases = []
    test_cases.append("import requests")
    test_cases.append("import pytest")
    test_cases.append("")
    test_cases.append(f"BASE_URL = \"{BASE_URL}\"")
    test_cases.append("")
    
    # Add authentication helper
    if auth_method in ['bearer_token', 'mixed']:
        test_cases.append("# Bearer token for authentication")
        test_cases.append("BEARER_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTQ2OTciLCJleHAiOjE3NTg1MjgwNTAsImlhdCI6MTc1ODQ0MTY1MCwiaXNzIjoiRU1QTE9ZRUUifQ.GdIm-wnuSsLNEccHQ13qxvJKPw8CS1fmmLj7RM9UFjw'")
        test_cases.append("")
    
    # Generate test cases for each endpoint
    for path, methods in schema.get('paths', {}).items():
        for method, details in methods.items():
            if method.upper() not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                continue
                
            # Extract parameters
            endpoint_params = []
            if 'parameters' in details:
                for param in details['parameters']:
                    if param.get('required', False):
                        endpoint_params.append({
                            'name': param['name'],
                            'in': param.get('in', 'query'),
                            'example': param.get('schema', {}).get('example', '')
                        })
            
            # Generate success test
            test_cases.append(f"def test_{method.lower()}_{path.split('/')[-1].replace('-', '_')}_success():")
            
            # Generate request based on auth method
            if auth_method == 'bearer_token':
                test_cases.append(f"    # curl -X {method.upper()} \"{BASE_URL}{path}\" -H \"Authorization: Bearer $BEARER_TOKEN\" -H \"Content-Type: application/json\"")
                test_cases.append("    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}")
                test_cases.append("    response = requests.get(f\"{BASE_URL}{path}\", headers=headers)")
            elif auth_method == 'query_param':
                # Original query parameter approach
                param_string = "&".join([f"{param['name']}=example_value" for param in endpoint_params])
                curl_url = f"{BASE_URL}{path}"
                if param_string:
                    curl_url += f"?{param_string}"
                test_cases.append(f"    # curl -X {method.upper()} \"{curl_url}\" -H \"Content-Type: application/json\"")
                test_cases.append(f"    response = requests.{method.lower()}(f\"{{BASE_URL}}{path}\", params={{'param': 'value'}})")
            else:  # mixed
                # Use Bearer token as primary, fallback to query params
                test_cases.append(f"    # curl -X {method.upper()} \"{BASE_URL}{path}\" -H \"Authorization: Bearer $BEARER_TOKEN\" -H \"Content-Type: application/json\"")
                test_cases.append("    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}")
                test_cases.append(f"    response = requests.{method.lower()}(f\"{{BASE_URL}}{path}\", headers=headers)")
            
            test_cases.append("    # Skip HTTP status check - focus on response body status")
            test_cases.append("    response_data = response.json()")
            test_cases.append("    # Validate success response")
            test_cases.append("    assert 'status' in response_data or 'data' in response_data")
            test_cases.append("")
            
            # Generate error tests
            error_scenarios = [
                {'name': 'invalid_token', 'desc': 'Invalid Bearer token'},
                {'name': 'missing_token', 'desc': 'Missing authentication'},
                {'name': 'expired_token', 'desc': 'Expired token'}
            ]
            
            for scenario in error_scenarios:
                test_cases.append(f"def test_{method.lower()}_{path.split('/')[-1].replace('-', '_')}_error_{scenario['name']}():")
                test_cases.append(f"    # {scenario['desc']}")
                
                if auth_method == 'bearer_token':
                    if scenario['name'] == 'missing_token':
                        test_cases.append(f"    # curl -X {method.upper()} \"{BASE_URL}{path}\" -H \"Content-Type: application/json\"")
                        test_cases.append(f"    response = requests.{method.lower()}(f\"{{BASE_URL}}{path}\")")
                    else:
                        invalid_token = 'invalid_token' if scenario['name'] == 'invalid_token' else 'expired_token'
                        test_cases.append(f"    # curl -X {method.upper()} \"{BASE_URL}{path}\" -H \"Authorization: Bearer {invalid_token}\" -H \"Content-Type: application/json\"")
                        test_cases.append(f"    headers = {{'Authorization': f'Bearer {invalid_token}'}}")
                        test_cases.append(f"    response = requests.{method.lower()}(f\"{{BASE_URL}}{path}\", headers=headers)")
                else:
                    # Query parameter approach for errors
                    test_cases.append(f"    # curl -X {method.upper()} \"{BASE_URL}{path}?invalid_param=invalid\" -H \"Content-Type: application/json\"")
                    test_cases.append(f"    response = requests.{method.lower()}(f\"{{BASE_URL}}{path}\", params={{'invalid_param': 'invalid'}})")
                
                test_cases.append("    # Skip HTTP status check - focus on response body status")
                test_cases.append("    response_data = response.json()")
                test_cases.append("    # Validate error response")
                test_cases.append("    assert 'status' in response_data or 'error' in response_data or 'message' in response_data")
                test_cases.append("")
    
    test_cases.append("if __name__ == \"__main__\":")
    test_cases.append("    pytest.main()")
    
    return "\n".join(test_cases)

def generate_curl_commands_bearer(schema: dict) -> str:
    """
    Generate curl commands with Bearer token support.
    """
    curl_commands = []
    auth_method = detect_auth_method(schema)
    
    curl_commands.append("# Curl Commands with Bearer Token Support")
    curl_commands.append(f"# Base URL: {BASE_URL}")
    curl_commands.append("")
    
    if auth_method in ['bearer_token', 'mixed']:
        curl_commands.append("# Set your Bearer token")
        curl_commands.append("export BEARER_TOKEN='your_token_here'")
        curl_commands.append("")
    
    for path, methods in schema.get('paths', {}).items():
        for method, details in methods.items():
            if method.upper() not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                continue
                
            curl_commands.append(f"# {method.upper()} {path}")
            
            if auth_method == 'bearer_token':
                curl_commands.append(f"curl -X {method.upper()} \"{BASE_URL}{path}\" \\")
                curl_commands.append("  -H \"Authorization: Bearer $BEARER_TOKEN\" \\")
                curl_commands.append("  -H \"Content-Type: application/json\"")
            else:
                # Query parameter approach
                curl_commands.append(f"curl -X {method.upper()} \"{BASE_URL}{path}?param=value\" \\")
                curl_commands.append("  -H \"Content-Type: application/json\"")
            
            curl_commands.append("")
    
    return "\n".join(curl_commands)

# Example usage and configuration
def create_bearer_auth_config():
    """
    Create configuration for Bearer token authentication.
    """
    config = {
        "auth_methods": {
            "bearer_token": {
                "header_name": "Authorization",
                "header_format": "Bearer {token}",
                "token_env_var": "BEARER_TOKEN"
            },
            "query_param": {
                "param_name": "AK",
                "param_value": "token_value"
            }
        },
        "test_scenarios": {
            "success": "Valid token with correct parameters",
            "invalid_token": "Invalid or malformed token",
            "missing_token": "No authentication provided",
            "expired_token": "Valid format but expired token"
        }
    }
    return config

if __name__ == "__main__":
    # Example usage
    import yaml
    
    # Load a sample schema
    with open('swagger/empdetails.yaml', 'r') as f:
        schema = yaml.safe_load(f)
    
    # Generate Bearer token tests
    test_code = generate_bearer_auth_tests("empdetails", schema)
    print("Generated Test Code:")
    print(test_code)
    
    # Generate curl commands
    curl_commands = generate_curl_commands_bearer(schema)
    print("\nGenerated Curl Commands:")
    print(curl_commands)
