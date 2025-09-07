import json
import os
import re
from openai import OpenAI
from .utils import BASE_URL

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_generated_code(code: str) -> str:
    """
    Clean up generated code by removing markdown formatting and explanations.
    """
    # Remove markdown code blocks
    code = re.sub(r'```python\s*\n?', '', code)
    code = re.sub(r'```\s*$', '', code)
    
    # Remove explanatory text before the first import
    lines = code.split('\n')
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            start_idx = i
            break
    
    # Remove explanatory text after the last Python statement
    end_idx = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('"""') and not lines[i].strip().startswith("'''"):
            if 'pytest.main()' in lines[i] or lines[i].strip() == 'if __name__ == "__main__":':
                end_idx = i + 1
                break
    
    # Extract only the Python code
    clean_lines = lines[start_idx:end_idx]
    
    # Remove any remaining markdown or explanatory text
    clean_code = '\n'.join(clean_lines)
    clean_code = re.sub(r'^# .*$', '', clean_code, flags=re.MULTILINE)
    clean_code = re.sub(r'^### .*$', '', clean_code, flags=re.MULTILINE)
    clean_code = re.sub(r'^Below is.*$', '', clean_code, flags=re.MULTILINE)
    
    return clean_code.strip()

def filter_undocumented_status_tests(test_code: str, status_codes: dict) -> str:
    """
    Filter out test functions that use undocumented status codes.
    """
    lines = test_code.split('\n')
    filtered_lines = []
    skip_function = False
    
    for line in lines:
        # Check if this is a function definition
        if line.strip().startswith('def test_'):
            skip_function = False
            # Check if this function uses undocumented status codes
            function_lines = []
            in_function = True
            i = lines.index(line)
            
            # Collect all lines of this function
            while i < len(lines) and in_function:
                current_line = lines[i]
                function_lines.append(current_line)
                
                # Check if we hit the next function or end of file
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if next_line.strip().startswith('def test_') or next_line.strip() == 'if __name__ == "__main__":':
                        in_function = False
                else:
                    in_function = False
                i += 1
            
            # Check if this function uses only documented status codes
            function_text = '\n'.join(function_lines)
            documented_only = True
            
            # Get all status codes for this endpoint (assuming single endpoint for simplicity)
            all_documented_codes = set()
            for endpoint_codes in status_codes.values():
                for method_codes in endpoint_codes.values():
                    all_documented_codes.update([str(code) for code in method_codes])
            
            # Check for undocumented status codes in assertions
            for status_code in ['401', '402', '400', '404', '403', '500']:
                if f'"{status_code}"' in function_text and status_code not in all_documented_codes:
                    documented_only = False
                    break
            
            if documented_only:
                filtered_lines.extend(function_lines)
            else:
                # Skip this function
                continue
        elif not line.strip().startswith('def test_') and not skip_function:
            filtered_lines.append(line)
    
    return '\n'.join(filtered_lines)

def extract_curl_commands(test_code: str) -> str:
    """
    Extract curl commands from test code and format them for easy copy-paste.
    """
    lines = test_code.split('\n')
    curl_commands = []
    
    for line in lines:
        if line.strip().startswith('# curl'):
            # Clean up the curl command
            curl_cmd = line.strip()[2:].strip()  # Remove '# ' prefix
            curl_commands.append(curl_cmd)
    
    return '\n'.join(curl_commands)

def extract_status_codes_from_spec(schema: dict) -> dict:
    """
    Extract all status codes defined in the OpenAPI specification.
    """
    status_codes = {}
    
    if 'paths' in schema:
        for path, methods in schema['paths'].items():
            status_codes[path] = {}
            for method, details in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    status_codes[path][method.upper()] = []
                    if 'responses' in details:
                        for status_code in details['responses'].keys():
                            # Handle both string and integer status codes
                            if isinstance(status_code, str) and status_code.isdigit():
                                status_codes[path][method.upper()].append(int(status_code))
                            elif isinstance(status_code, int):
                                status_codes[path][method.upper()].append(status_code)
    
    return status_codes

def extract_required_parameters(schema: dict) -> dict:
    """
    Extract required parameters from the OpenAPI specification.
    """
    required_params = {}
    
    if 'paths' in schema:
        for path, methods in schema['paths'].items():
            required_params[path] = {}
            for method, details in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    required_params[path][method.upper()] = []
                    if 'parameters' in details:
                        for param in details['parameters']:
                            if param.get('required', False):
                                required_params[path][method.upper()].append({
                                    'name': param['name'],
                                    'example': param.get('example', ''),
                                    'description': param.get('description', '')
                                })
    
    return required_params

def extract_response_schemas(schema: dict) -> dict:
    """
    Extract response schemas and examples from the OpenAPI specification.
    """
    response_schemas = {}
    
    if 'paths' in schema:
        for path, methods in schema['paths'].items():
            response_schemas[path] = {}
            for method, details in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    response_schemas[path][method.upper()] = {}
                    if 'responses' in details:
                        for status_code, response_info in details['responses'].items():
                            # Handle both string and integer status codes
                            if isinstance(status_code, str) and status_code.isdigit():
                                response_schemas[path][method.upper()][int(status_code)] = {
                                    'description': response_info.get('description', ''),
                                    'schema': response_info.get('content', {}).get('application/json', {}).get('schema', {}),
                                    'examples': response_info.get('content', {}).get('application/json', {}).get('examples', {})
                                }
                            elif isinstance(status_code, int):
                                response_schemas[path][method.upper()][status_code] = {
                                    'description': response_info.get('description', ''),
                                    'schema': response_info.get('content', {}).get('application/json', {}).get('schema', {}),
                                    'examples': response_info.get('content', {}).get('application/json', {}).get('examples', {})
                                }
    
    return response_schemas

def extract_schema_properties(schema: dict, components: dict = None) -> dict:
    """
    Recursively extract properties from a schema, resolving $ref references.
    """
    if not schema:
        return {}
    
    properties = {}
    
    # Handle $ref references
    if '$ref' in schema:
        ref_path = schema['$ref']
        if ref_path.startswith('#/components/schemas/'):
            schema_name = ref_path.split('/')[-1]
            if components and 'schemas' in components and schema_name in components['schemas']:
                return extract_schema_properties(components['schemas'][schema_name], components)
        return {}
    
    # Handle direct properties
    if 'properties' in schema:
        for prop_name, prop_schema in schema['properties'].items():
            properties[prop_name] = {
                'type': prop_schema.get('type', 'string'),
                'example': prop_schema.get('example', ''),
                'description': prop_schema.get('description', '')
            }
    
    # Handle array items
    if schema.get('type') == 'array' and 'items' in schema:
        items_schema = schema['items']
        if '$ref' in items_schema:
            ref_path = items_schema['$ref']
            if ref_path.startswith('#/components/schemas/'):
                schema_name = ref_path.split('/')[-1]
                if components and 'schemas' in components and schema_name in components['schemas']:
                    properties = extract_schema_properties(components['schemas'][schema_name], components)
        elif 'properties' in items_schema:
            properties = extract_schema_properties(items_schema, components)
    
    # Handle oneOf schemas
    if 'oneOf' in schema:
        for one_of_schema in schema['oneOf']:
            one_of_props = extract_schema_properties(one_of_schema, components)
            properties.update(one_of_props)
    
    return properties

def generate_response_validation_code(response_schema: dict, status_code: int) -> str:
    """
    Generate Python code to validate response structure based on schema.
    """
    if not response_schema or 'schema' not in response_schema:
        return f"    # No specific validation for status {status_code}"
    
    schema = response_schema['schema']
    examples = response_schema.get('examples', {})
    
    validation_code = []
    
    # Handle array responses
    if schema.get('type') == 'array':
        validation_code.append("    response_data = response.json()")
        validation_code.append("    assert isinstance(response_data, list)")
        
        if 'items' in schema:
            items_schema = schema['items']
            if '$ref' in items_schema:
                # Extract properties from referenced schema
                ref_path = items_schema['$ref']
                if ref_path.startswith('#/components/schemas/'):
                    schema_name = ref_path.split('/')[-1]
                    validation_code.append(f"    # Validating array items against {schema_name} schema")
                    validation_code.append("    if response_data:  # Only validate if array is not empty")
                    validation_code.append("        item = response_data[0]")
                    validation_code.append("        # Add specific field validations based on schema")
            elif 'properties' in items_schema:
                validation_code.append("    if response_data:  # Only validate if array is not empty")
                validation_code.append("        item = response_data[0]")
                for prop_name, prop_info in items_schema['properties'].items():
                    if prop_name in ['EMPLOYEENAME', 'EMAIL', 'MOBILE', 'EMPLOYEEID']:
                        validation_code.append(f"        assert '{prop_name}' in item")
    
    # Handle object responses
    elif schema.get('type') == 'object':
        validation_code.append("    response_data = response.json()")
        validation_code.append("    assert isinstance(response_data, dict)")
        
        # Check for status field pattern
        if 'properties' in schema and 'status' in schema['properties']:
            validation_code.append("    if 'status' in response_data:")
            validation_code.append(f"        assert response_data['status'] == '{status_code}'")
            validation_code.append("    else:")
            validation_code.append("        # Direct data response - validate expected fields")
            # Add field validations based on examples
            for example_name, example_data in examples.items():
                if isinstance(example_data.get('value'), dict):
                    for field in example_data['value'].keys():
                        if field in ['EMPLOYEENAME', 'EMAIL', 'MOBILE', 'EMPLOYEEID']:
                            validation_code.append(f"        assert '{field}' in response_data")
    
    # Handle direct field responses (like the current empd API)
    else:
        validation_code.append("    response_data = response.json()")
        validation_code.append("    # Validate based on actual response structure")
        validation_code.append("    if 'status' in response_data:")
        validation_code.append(f"        assert response_data['status'] == '{status_code}'")
        validation_code.append("    else:")
        validation_code.append("        # Direct data response")
        validation_code.append("        assert 'EMPLOYEENAME' in response_data")
        validation_code.append("        assert 'EMAIL' in response_data")
    
    return '\n'.join(validation_code)

def generate_dynamic_tests(api_name: str, schema: dict) -> str:
    """
    Generate pytest test cases using dynamic response handling based on Swagger schemas.
    """
    # Extract status codes, required parameters, and response schemas from the spec
    status_codes = extract_status_codes_from_spec(schema)
    required_params = extract_required_parameters(schema)
    response_schemas = extract_response_schemas(schema)
    api_pattern = detect_api_pattern(schema)
    
    # Generate test cases based on the actual API structure
    test_cases = []
    
    # Add imports
    test_cases.append("import requests")
    test_cases.append("import pytest")
    test_cases.append("")
    test_cases.append(f"BASE_URL = \"{BASE_URL}\"")
    test_cases.append("")
    
    # Generate test cases for each endpoint
    for path, methods in schema.get('paths', {}).items():
        for method, details in methods.items():
            if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                # Get required parameters for this endpoint
                endpoint_params = required_params.get(path, {}).get(method.upper(), [])
                
                # Get response schemas for this endpoint
                endpoint_responses = response_schemas.get(path, {}).get(method.upper(), {})
                
                # Generate test cases based on documented status codes
                for status_code in status_codes.get(path, {}).get(method.upper(), []):
                    # Generate different test scenarios based on status code
                    if status_code == 200:
                        # Success case - use valid parameters
                        test_name = f"test_{method.lower()}_{path.split('/')[-1].replace('{', '').replace('}', '').replace('-', '_')}_success"
                        test_scenario = "success"
                    else:
                        # Error case - use invalid/missing parameters
                        test_name = f"test_{method.lower()}_{path.split('/')[-1].replace('{', '').replace('}', '').replace('-', '_')}_error_{status_code}"
                        test_scenario = "error"
                    
                    # Generate curl command and request based on scenario
                    if test_scenario == "success":
                        # Success case - use all required parameters with valid values
                        request_params = {}
                        for param in endpoint_params:
                            # Use the example value from the spec, or a default valid value
                            if param['example']:
                                request_params[param['name']] = param['example']
                            else:
                                # Provide default valid values for common parameters
                                if param['name'] == 'empid':
                                    request_params[param['name']] = '114697'
                                elif param['name'] == 'AK':
                                    request_params[param['name']] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTQ2OTciLCJleHAiOjE3NTg1MjgwNTAsImlhdCI6MTc1ODQ0MTY1MCwiaXNzIjoiRU1QTE9ZRUUifQ.GdIm-wnuSsLNEccHQ13qxvJKPw8CS1fmmLj7RM9UFjw'
                                elif param['name'] == 'keyword':
                                    request_params[param['name']] = 'test'
                                else:
                                    request_params[param['name']] = 'valid_value'
                        
                        param_string = "&".join([f"{param['name']}={request_params[param['name']]}" for param in endpoint_params])
                        curl_url = f"{BASE_URL}{path}"
                        if param_string:
                            curl_url += f"?{param_string}"
                        
                        curl_comment = f"    # curl -X {method.upper()} \"{curl_url}\" -H \"Content-Type: application/json\""
                        
                        if request_params:
                            request_code = f"    response = requests.{method.lower()}(f\"{{BASE_URL}}{path}\", params={request_params})"
                        else:
                            request_code = f"    response = requests.{method.lower()}(f\"{{BASE_URL}}{path}\")"
                        
                        # For success case, skip HTTP status check
                        status_assertion = "    # Skip HTTP status check - focus on response body status"
                        
                    else:
                        # Error case - use invalid/missing parameters
                        if endpoint_params:
                            # Use invalid values for required parameters
                            invalid_params = {}
                            for param in endpoint_params:
                                if param['name'] == 'AK':
                                    invalid_params[param['name']] = 'invalid_token'
                                elif param['name'] == 'empid':
                                    invalid_params[param['name']] = 'invalid_id'
                                else:
                                    invalid_params[param['name']] = 'invalid_value'
                            
                            param_string = "&".join([f"{param['name']}={invalid_params.get(param['name'], 'invalid')}" for param in endpoint_params])
                            curl_url = f"{BASE_URL}{path}"
                            if param_string:
                                curl_url += f"?{param_string}"
                            
                            curl_comment = f"    # curl -X {method.upper()} \"{curl_url}\" -H \"Content-Type: application/json\""
                            request_code = f"    response = requests.{method.lower()}(f\"{{BASE_URL}}{path}\", params={invalid_params})"
                        else:
                            # No required parameters, just call the endpoint
                            curl_url = f"{BASE_URL}{path}"
                            curl_comment = f"    # curl -X {method.upper()} \"{curl_url}\" -H \"Content-Type: application/json\""
                            request_code = f"    response = requests.{method.lower()}(f\"{{BASE_URL}}{path}\")"
                        
                        # Skip HTTP status check - focus on response body status
                        status_assertion = "    # Skip HTTP status check - focus on response body status"
                    
                    # Generate response validation based on schema
                    response_validation = generate_response_validation_for_endpoint(
                        endpoint_responses.get(status_code, {}), 
                        status_code, 
                        api_pattern,
                        test_scenario
                    )
                    
                    # Combine test case
                    test_case = [
                        f"def {test_name}():",
                        curl_comment,
                        request_code,
                        status_assertion,
                        response_validation,
                        ""
                    ]
                    
                    test_cases.extend(test_case)
    
    return "\n".join(test_cases)

def generate_response_validation_for_endpoint(response_schema: dict, status_code: int, api_pattern: str, test_scenario: str = "success") -> str:
    """
    Generate response validation code based on the specific response schema.
    """
    if not response_schema or 'schema' not in response_schema:
        return f"    # No specific validation for status {status_code}"
    
    schema = response_schema['schema']
    examples = response_schema.get('examples', {})
    
    validation_lines = []
    validation_lines.append("    response_data = response.json()")
    
    # Always validate status codes in response body (all APIs use this pattern)
    validation_lines.append(f"    # Validate response for status {status_code} in response body")
    validation_lines.append("    # Check status in response body")
    validation_lines.append("    if isinstance(response_data, list) and response_data:")
    validation_lines.append("        item = response_data[0]")
    validation_lines.append("        assert 'status' in item")
    validation_lines.append(f"        # Handle both string and integer status codes")
    validation_lines.append(f"        assert item['status'] == {status_code} or item['status'] == '{status_code}'")
    validation_lines.append("        assert 'data' in item")
    validation_lines.append("    else:")
    validation_lines.append("        # Handle direct response")
    validation_lines.append("        assert 'status' in response_data")
    validation_lines.append(f"        # Handle both string and integer status codes")
    validation_lines.append(f"        assert response_data['status'] == {status_code} or response_data['status'] == '{status_code}'")
    
    return "\n".join(validation_lines)

def detect_api_pattern(schema: dict) -> str:
    """
    Detect if the API uses HTTP status codes or response body status pattern.
    """
    # Check for specific patterns that indicate response body status
    has_status_in_body = False
    
    # Check response examples for status in body pattern
    for path, methods in schema.get('paths', {}).items():
        for method, details in methods.items():
            if 'responses' in details:
                for status_code, response_info in details['responses'].items():
                    # Handle both string and integer status codes
                    if (isinstance(status_code, str) and status_code.isdigit()) or isinstance(status_code, int):
                        content = response_info.get('content', {}).get('application/json', {})
                        
                        # Check examples for status in body pattern
                        if 'examples' in content:
                            for example_name, example_data in content['examples'].items():
                                if isinstance(example_data.get('value'), dict):
                                    if 'status' in example_data['value'] and 'message' in example_data['value']:
                                        has_status_in_body = True
                                        break
                        
                        # Check schema for status field pattern
                        if 'schema' in content:
                            schema_def = content['schema']
                            if schema_def.get('type') == 'array' and 'items' in schema_def:
                                items_schema = schema_def['items']
                                if '$ref' in items_schema:
                                    ref_path = items_schema['$ref']
                                    if ref_path.startswith('#/components/schemas/'):
                                        schema_name = ref_path.split('/')[-1]
                                        if 'components' in schema and 'schemas' in schema['components']:
                                            ref_schema = schema['components']['schemas'].get(schema_name, {})
                                            if 'properties' in ref_schema and 'status' in ref_schema['properties']:
                                                has_status_in_body = True
                                                break
                            elif 'properties' in schema_def and 'status' in schema_def['properties']:
                                has_status_in_body = True
                                break
                        
                        if has_status_in_body:
                            break
                    if has_status_in_body:
                        break
                if has_status_in_body:
                    break
            if has_status_in_body:
                break
        if has_status_in_body:
            break
    
    if has_status_in_body:
        return "response_body_status"
    
    return "http_status_codes"

def generate_tests(api_name: str, schema: dict) -> str:
    """
    Generate pytest test cases for a given API schema using dynamic response handling.
    """
    # Use the new dynamic test generator instead of LLM
    return generate_dynamic_tests(api_name, schema)

def generate_tests_llm(api_name: str, schema: dict) -> str:
    """
    Use LLM to generate pytest test cases for a given API schema (fallback method).
    """
    # Extract status codes, required parameters, and response schemas from the spec
    status_codes = extract_status_codes_from_spec(schema)
    required_params = extract_required_parameters(schema)
    response_schemas = extract_response_schemas(schema)
    api_pattern = detect_api_pattern(schema)
    
    # Determine status checking pattern
    if api_pattern == "response_body_status":
        status_instruction = """
    STATUS CODE HANDLING FOR THIS API:
    - This API returns HTTP 200 but may include status in response body
    - Always check: assert response.status_code == 200
    - Handle two response patterns:
      1. Success: Direct data (e.g., {{"EMPLOYEENAME": "John", "EMAIL": "john@example.com"}})
      2. Error: Status in body (e.g., {{"status": "401", "message": "Token Expired", "data": []}})
    - Check response structure: if "status" in response.json() then check status field
    - If no status field, verify expected data fields are present directly in response.json()
    - Do NOT assume nested data structures like response.json()[0]["data"][0]
        """
    else:
        status_instruction = """
    STATUS CODE HANDLING FOR THIS API:
    - This API returns different HTTP status codes directly
    - Check HTTP status: assert response.status_code == 200
        """
    
    prompt = f"""
    You are a QA engineer. Given this OpenAPI spec for {api_name}:
    {json.dumps(schema)[:4000]}

    AVAILABLE STATUS CODES BY ENDPOINT:
    {json.dumps(status_codes, indent=2)}

    REQUIRED PARAMETERS BY ENDPOINT:
    {json.dumps(required_params, indent=2)}

    RESPONSE SCHEMAS BY ENDPOINT:
    {json.dumps(response_schemas, indent=2)}

    Generate ONLY Python pytest test cases using 'requests'. Do NOT include any markdown formatting, explanations, or code blocks.
    
    CRITICAL REQUIREMENTS:
    - ONLY use status codes that are explicitly listed above for each endpoint
    - ONLY test endpoints and parameters that are defined in the spec
    - ALWAYS include ALL required parameters from the REQUIRED PARAMETERS list above
    - Use the example values provided in the spec for required parameters
    - VALIDATE RESPONSE STRUCTURE based on the RESPONSE SCHEMAS above
    - Handle different response patterns: arrays, objects, status objects, direct data
    - Use the examples from the response schemas to validate actual response fields
    - Do NOT assume or generate status codes not mentioned in the spec
    - Do NOT create test cases for scenarios not covered in the spec
    - If the spec only defines "200" status, ONLY generate tests expecting "200" status
    - Do NOT generate tests for "401", "402", "400", "404" unless they are in the AVAILABLE STATUS CODES list above
    - Start directly with import statements
    - Use BASE_URL = "{BASE_URL}" at the top
    
    {status_instruction}
    
    - For each test function, add a comment with the equivalent curl command
    - Use actual parameter values in curl commands (not placeholders)
    - Format curl commands as: # curl -X METHOD "BASE_URL/endpoint?param1=value1&param2=value2" -H "Content-Type: application/json"
    - For POST/PUT requests, include -d '{{"json": "data"}}' in curl commands
    - End with if __name__ == "__main__": pytest.main()
    - Return ONLY the Python code, no markdown, no explanations, no code blocks
    
    IMPORTANT: Only generate tests for the exact endpoints, methods, and status codes defined in the OpenAPI specification. Do not make assumptions about error codes or edge cases not documented in the spec.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4/gpt-5 if available
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    # Clean the generated code to remove any markdown formatting
    raw_code = response.choices[0].message.content
    clean_code = clean_generated_code(raw_code)
    
    # Filter out tests with undocumented status codes
    clean_code = filter_undocumented_status_tests(clean_code, status_codes)
    
    return clean_code
