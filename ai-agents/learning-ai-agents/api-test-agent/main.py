import sys
from agent.utils import load_swagger, ensure_dirs, get_paths
from agent.generator import generate_tests, extract_curl_commands
from agent.runner import run_tests

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <api_name>")
        sys.exit(1)

    api_name = sys.argv[1]
    print(f"[INFO] Running agent for API: {api_name}")

    # Prepare dirs
    ensure_dirs(api_name)
    paths = get_paths(api_name)

    # Load swagger spec
    schema = load_swagger(api_name)

    # Generate tests
    test_code = generate_tests(api_name, schema)
    with open(paths["test_file"], "w") as f:
        f.write(test_code)
    print(f"[INFO] Test file created: {paths['test_file']}")

    # Generate curl commands file
    curl_commands = extract_curl_commands(test_code)
    curl_file = f"curl_commands_{api_name}.txt"
    with open(curl_file, "w") as f:
        f.write(f"# Curl commands for {api_name} API testing\n")
        f.write(f"# Base URL: {load_swagger(api_name).get('servers', [{}])[0].get('url', 'https://merp.intermesh.net')}\n\n")
        f.write(curl_commands)
    print(f"[INFO] Curl commands file created: {curl_file}")

    # Run tests
    run_tests(paths["test_file"], paths["result_file"])

if __name__ == "__main__":
    main()
