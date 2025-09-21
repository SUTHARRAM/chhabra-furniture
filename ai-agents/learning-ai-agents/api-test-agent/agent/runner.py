import subprocess
import re
from pathlib import Path
from datetime import datetime

def run_tests(test_file: str, result_file: str):
    """Run pytest on given file and save results."""
    result = subprocess.run(
        ["pytest", test_file, "-v"],
        capture_output=True,
        text=True
    )
    
    # Generate human-readable results
    human_readable_results = generate_human_readable_results(result, test_file)
    
    Path(result_file).write_text(human_readable_results)
    print(f"[INFO] Results saved to {result_file}")

def generate_human_readable_results(result, test_file):
    """Generate human-readable test results."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    api_name = Path(test_file).parent.name
    
    # Parse test results
    stdout_lines = result.stdout.split('\n')
    stderr_lines = result.stderr.split('\n')
    
    # Count results
    passed_tests = []
    failed_tests = []
    error_tests = []
    
    # Parse test results from stdout
    for line in stdout_lines:
        if 'PASSED' in line:
            test_name = extract_test_name(line)
            if test_name:
                passed_tests.append(test_name)
        elif 'FAILED' in line:
            test_name = extract_test_name(line)
            if test_name:
                failed_tests.append(test_name)
        elif 'ERROR' in line:
            test_name = extract_test_name(line)
            if test_name:
                error_tests.append(test_name)
    
    # Generate human-readable report
    report = f"""
{'='*80}
API TEST REPORT - {api_name.upper()}
{'='*80}
Generated on: {timestamp}
Test File: {test_file}

📊 SUMMARY
{'='*40}
✅ PASSED: {len(passed_tests)} tests
❌ FAILED: {len(failed_tests)} tests
⚠️  ERRORS: {len(error_tests)} tests
📈 TOTAL: {len(passed_tests) + len(failed_tests) + len(error_tests)} tests

"""
    
    # Add passed tests section
    if passed_tests:
        report += f"""
✅ PASSED TESTS ({len(passed_tests)})
{'='*40}
"""
        for i, test in enumerate(passed_tests, 1):
            report += f"{i}. {format_test_name(test)}\n"
        report += "\n"
    
    # Add failed tests section
    if failed_tests:
        report += f"""
❌ FAILED TESTS ({len(failed_tests)})
{'='*40}
"""
        for i, test in enumerate(failed_tests, 1):
            report += f"{i}. {format_test_name(test)}\n"
        report += "\n"
    
    # Add error tests section
    if error_tests:
        report += f"""
⚠️  ERROR TESTS ({len(error_tests)})
{'='*40}
"""
        for i, test in enumerate(error_tests, 1):
            report += f"{i}. {format_test_name(test)}\n"
        report += "\n"
    
    # Add detailed error information
    if result.stderr.strip():
        report += f"""
🔍 DETAILED ERROR INFORMATION
{'='*40}
{result.stderr}
"""
    
    # Add raw pytest output for technical reference
    report += f"""
📋 TECHNICAL DETAILS (for developers)
{'='*40}
STDOUT:
{result.stdout}

STDERR:
{result.stderr}
"""
    
    return report

def extract_test_name(line):
    """Extract test name from pytest output line."""
    # Match patterns like: tests/gluser/test_gluser.py::test_get_glid_details_success PASSED
    match = re.search(r'::([^:\s]+)\s+(PASSED|FAILED|ERROR)', line)
    return match.group(1) if match else None

def format_test_name(test_name):
    """Format test name to be more human-readable."""
    # Convert snake_case to Title Case
    formatted = test_name.replace('_', ' ').title()
    
    # Add some context based on test name
    if 'valid' in test_name.lower():
        formatted += " (Valid Input Test)"
    elif 'invalid' in test_name.lower():
        formatted += " (Invalid Input Test)"
    elif 'auth' in test_name.lower() or 'token' in test_name.lower():
        formatted += " (Authentication Test)"
    elif 'no_' in test_name.lower() or 'missing' in test_name.lower():
        formatted += " (Missing Data Test)"
    elif 'expired' in test_name.lower():
        formatted += " (Expired Token Test)"
    elif 'optional' in test_name.lower():
        formatted += " (Optional Parameters Test)"
    
    return formatted
