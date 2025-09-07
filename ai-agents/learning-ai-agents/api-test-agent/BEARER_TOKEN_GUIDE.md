# Bearer Token Authentication Support

This guide explains how to use the enhanced API test agent with Bearer token authentication.

## Overview

The enhanced agent supports multiple authentication methods:
- **Query Parameters**: `?AK=token` (original method)
- **Bearer Tokens**: `Authorization: Bearer token` (new method)
- **Auto-detection**: Automatically detects the authentication method from Swagger specs

## Quick Start

### 1. Basic Usage

```bash
# Auto-detect authentication method
python enhanced_main.py your_api

# Force Bearer token authentication
python enhanced_main.py your_api --auth-method bearer_token

# Force query parameter authentication
python enhanced_main.py your_api --auth-method query_param
```

### 2. Generated Test Structure

#### Bearer Token Tests
```python
import requests
import pytest

BASE_URL = "https://api.example.com"
BEARER_TOKEN = 'your_token_here'

def test_get_endpoint_success():
    # curl -X GET "https://api.example.com/endpoint" -H "Authorization: Bearer $BEARER_TOKEN"
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    response = requests.get(f"{BASE_URL}/endpoint", headers=headers)
    response_data = response.json()
    assert 'status' in response_data or 'data' in response_data

def test_get_endpoint_error_invalid_token():
    headers = {'Authorization': f'Bearer invalid_token'}
    response = requests.get(f"{BASE_URL}/endpoint", headers=headers)
    response_data = response.json()
    assert 'status' in response_data or 'error' in response_data
```

#### Query Parameter Tests (Original)
```python
def test_get_endpoint_success():
    # curl -X GET "https://api.example.com/endpoint?AK=token"
    response = requests.get(f"{BASE_URL}/endpoint", params={'AK': 'token'})
    response_data = response.json()
    assert 'status' in response_data or 'data' in response_data
```

## Swagger Specification Requirements

### For Bearer Token Authentication

Your Swagger spec should include:

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: "JWT token obtained from /auth/login endpoint"

security:
  - bearerAuth: []

paths:
  /your-endpoint:
    get:
      security:
        - bearerAuth: []
      responses:
        '200':
          description: Success
        '401':
          description: Unauthorized
```

### For Query Parameter Authentication

```yaml
paths:
  /your-endpoint:
    get:
      parameters:
        - name: AK
          in: query
          required: true
          schema:
            type: string
            example: "your_token_here"
```

## Authentication Method Detection

The agent automatically detects authentication methods by analyzing:

1. **Security Schemes**: Looks for `http` + `bearer` schemes
2. **Parameters**: Checks for `Authorization` header parameters
3. **Query Parameters**: Looks for auth-related query params like `AK`, `token`, `auth_token`

## Generated Test Scenarios

### Success Scenarios
- Valid token with correct parameters
- Proper response validation

### Error Scenarios
- **Invalid Token**: Malformed or incorrect token
- **Missing Token**: No authentication provided
- **Expired Token**: Valid format but expired token

## Curl Commands

The agent generates ready-to-use curl commands:

### Bearer Token
```bash
export BEARER_TOKEN='your_token_here'
curl -X GET "https://api.example.com/endpoint" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -H "Content-Type: application/json"
```

### Query Parameter
```bash
curl -X GET "https://api.example.com/endpoint?AK=your_token" \
  -H "Content-Type: application/json"
```

## Configuration

### Environment Variables
```bash
# For Bearer tokens
export BEARER_TOKEN='your_actual_token'

# For query parameters
export AUTH_TOKEN='your_actual_token'
```

### Token Management
- Store tokens in `.env` files
- Use different tokens for different environments
- Rotate tokens regularly for security

## Examples

### Example 1: JWT Bearer Token API
```yaml
# swagger/jwt_api.yaml
openapi: 3.0.0
info:
  title: JWT API
  version: 1.0.0
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
security:
  - bearerAuth: []
```

```bash
python enhanced_main.py jwt_api --auth-method bearer_token
```

### Example 2: Mixed Authentication API
```yaml
# Some endpoints use Bearer, others use query params
paths:
  /secure-endpoint:
    get:
      security:
        - bearerAuth: []
  /legacy-endpoint:
    get:
      parameters:
        - name: AK
          in: query
          required: true
```

```bash
python enhanced_main.py mixed_api --auth-method auto
```

## Best Practices

### 1. Token Security
- Never commit tokens to version control
- Use environment variables
- Implement token rotation

### 2. Test Data
- Use test-specific tokens
- Mock external authentication services
- Test with both valid and invalid tokens

### 3. Error Handling
- Test all authentication failure scenarios
- Validate error response formats
- Check proper HTTP status codes

### 4. Documentation
- Document authentication requirements
- Provide token generation instructions
- Include troubleshooting guides

## Troubleshooting

### Common Issues

1. **"No authentication method detected"**
   - Check your Swagger spec has proper security schemes
   - Ensure parameters are marked as required

2. **"Token not found"**
   - Set the BEARER_TOKEN environment variable
   - Check token format and validity

3. **"Test failures"**
   - Verify API endpoint URLs
   - Check token permissions
   - Validate response format expectations

### Debug Mode
```bash
# Enable verbose output
python enhanced_main.py your_api --auth-method bearer_token -v
```

## Migration from Query Parameters

If you're migrating from query parameter to Bearer token authentication:

1. Update your Swagger spec
2. Regenerate tests with `--auth-method bearer_token`
3. Update your API client code
4. Test thoroughly with both methods

## Support

For issues or questions:
1. Check the generated test files
2. Verify your Swagger specification
3. Test with manual curl commands
4. Review the authentication method detection logic
