# API Test Agent

An AI-powered agent that automatically generates and runs pytest test cases for REST APIs based on OpenAPI/Swagger specifications.

## Features

- 🤖 **AI-Powered Test Generation**: Uses OpenAI's GPT models to generate comprehensive test cases
- 📋 **OpenAPI Support**: Works with Swagger/OpenAPI 3.0 specifications
- 🧪 **Pytest Integration**: Generates pytest-compatible test files
- 📊 **Test Results**: Captures and saves test execution results
- 🔧 **Modular Design**: Clean separation of concerns with dedicated modules

## Project Structure

```
api-test-agent/
├── agent/                    # Core agent logic
│   ├── __init__.py
│   ├── generator.py          # LLM-based test generator
│   ├── runner.py             # Run pytest & capture results
│   └── utils.py              # Helpers (load swagger, paths, etc.)
├── swagger/                  # All Swagger/OpenAPI YAML specs
│   ├── orders.yaml
│   ├── users.yaml
│   └── inventory.yaml
├── tests/                    # Generated test cases (per API)
│   ├── orders/
│   │   └── test_orders.py
│   └── users/
│       └── test_users.py
├── results/                  # Test run results
│   ├── orders.txt
│   └── users.txt
├── main.py                   # Entrypoint script
├── requirements.txt
└── README.md
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd api-test-agent
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file and add your OpenAI API key
   nano .env
   ```
   
   Or set the environment variable directly:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Usage

### Basic Usage

Run the agent for a specific API:

```bash
python main.py <api_name>
```

**Examples**:
```bash
# Generate tests for orders API
python main.py orders

# Generate tests for users API
python main.py users

# Generate tests for inventory API
python main.py inventory
```

### How It Works

1. **Load Swagger Spec**: The agent loads the OpenAPI specification from `swagger/{api_name}.yaml`
2. **Generate Tests**: Uses OpenAI's GPT to generate comprehensive pytest test cases
3. **Save Tests**: Writes the generated tests to `tests/{api_name}/test_{api_name}.py`
4. **Run Tests**: Executes pytest and captures results
5. **Save Results**: Stores test results in `results/{api_name}.txt`

## Configuration

### Environment Variables

The application uses environment variables for configuration. Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

**Required Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key (get from https://platform.openai.com/api-keys)
- `BASE_URL`: The base URL for your API (default: https://merp.intermesh.net)

### Base URL

The base URL can be configured in the `.env` file:

```bash
BASE_URL=https://your-api-base-url.com
```

Or you can modify it directly in `agent/utils.py`:

```python
BASE_URL = os.getenv("BASE_URL", "https://your-api-base-url.com")
```

### OpenAI Model

The default model is `gpt-4o-mini`. You can change this in `agent/generator.py`:

```python
response = client.chat.completions.create(
    model="gpt-4",  # Change to your preferred model
    # ...
)
```

## Adding New APIs

1. **Add Swagger Spec**: Place your OpenAPI YAML file in the `swagger/` directory
2. **Run Agent**: Execute `python main.py <your-api-name>`
3. **Review Tests**: Check the generated tests in `tests/{api_name}/`
4. **Check Results**: Review test execution results in `results/{api_name}.txt`

## Generated Test Features

The AI agent generates tests that include:

- ✅ **Specification-Based Testing**: Only tests endpoints and status codes defined in the OpenAPI spec
- ✅ **Positive Test Cases**: Valid requests with expected responses
- ❌ **Negative Test Cases**: Invalid requests and error handling (only for documented error codes)
- 🔍 **Accurate Status Codes**: Uses only status codes explicitly defined in the Swagger specification
- 📝 **No Assumptions**: Does not generate tests for undocumented scenarios or error codes
- 📊 **Response Validation**: Basic response structure validation
- 🔗 **Curl Commands**: Ready-to-use curl commands for manual testing
- 📋 **Human-Readable Reports**: Easy-to-understand test results for non-technical users
- 🔄 **Dual Response Pattern Handling**: Automatically detects and handles APIs that return different response structures for success vs error cases
- 🔑 **Required Parameters**: Automatically includes all required parameters from the OpenAPI specification
- 📋 **Accurate Response Validation**: Handles different response structures (direct data vs status objects)
- 🎯 **Dynamic Response Handling**: Generates test cases based on actual Swagger response schemas and examples
- 🔍 **Schema-Based Validation**: Uses OpenAPI schema definitions to validate response structure and fields
- 📊 **Pattern Detection**: Automatically detects API response patterns (HTTP status codes vs response body status)

## Dynamic Response Handling

The API Test Agent now features advanced dynamic response handling that automatically adapts to different API patterns:

### 🎯 **Automatic Pattern Detection**
- **HTTP Status Codes**: Standard REST APIs that return different HTTP status codes (200, 201, 400, 404, etc.)
- **Response Body Status**: APIs that always return HTTP 200 but include status information in the response body

### 🔍 **Schema-Based Validation**
- Extracts response schemas directly from OpenAPI specifications
- Uses actual response examples to generate accurate field validations
- Handles different response types: arrays, objects, nested structures
- Validates specific fields based on schema definitions

### 📊 **Response Structure Examples**

**Standard HTTP Status Pattern:**
```python
def test_get_users_200():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    if response_data:
        item = response_data[0]
        assert 'id' in item
        assert 'username' in item
```

**Response Body Status Pattern:**
```python
def test_get_employee_details_200():
    response = requests.get(f"{BASE_URL}/api/employee", params={"id": "123"})
    assert response.status_code == 200
    response_data = response.json()
    
    if 'status' in response_data:
        # Error case - status in response body
        assert response_data['status'] == '200'
        assert 'message' in response_data
    else:
        # Success case - direct data
        assert 'EMPLOYEENAME' in response_data
        assert 'EMAIL' in response_data
```

## Test Results Format

The agent generates comprehensive, human-readable test reports that include:

### 📊 Summary Section
- Clear pass/fail/error counts with emojis
- Success rate percentage
- Total test count

### ✅ Passed Tests
- List of successful tests with descriptive names
- Context about what each test validates

### ❌ Failed Tests  
- List of failed tests with clear descriptions
- Categorized by test type (Authentication, Invalid Input, etc.)

### 🔍 Detailed Information
- Technical details for developers
- Raw pytest output for debugging
- Specific error messages and assertions

### 📋 Summary Report
Run `python3 generate_summary.py` to generate an overall summary across all APIs.

## Dependencies

- **openai**: For AI-powered test generation
- **pytest**: For running generated tests
- **requests**: For making HTTP requests in tests
- **pyyaml**: For parsing OpenAPI specifications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue on the GitHub repository.
