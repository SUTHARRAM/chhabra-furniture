#!/usr/bin/env python3
"""
Generate a summary report for all API test results.
"""

import os
import re
from pathlib import Path
from datetime import datetime

def generate_summary_report():
    """Generate a summary report for all API test results."""
    results_dir = Path("results")
    if not results_dir.exists():
        print("No results directory found!")
        return
    
    # Find all result files
    result_files = list(results_dir.glob("*.txt"))
    if not result_files:
        print("No result files found!")
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate summary report
    report = f"""
{'='*80}
API TESTING SUMMARY REPORT
{'='*80}
Generated on: {timestamp}
Total APIs Tested: {len(result_files)}

"""
    
    total_passed = 0
    total_failed = 0
    total_errors = 0
    total_tests = 0
    
    api_summaries = []
    
    for result_file in sorted(result_files):
        api_name = result_file.stem
        content = result_file.read_text()
        
        # Extract summary information
        passed_match = re.search(r'✅ PASSED: (\d+) tests', content)
        failed_match = re.search(r'❌ FAILED: (\d+) tests', content)
        error_match = re.search(r'⚠️  ERRORS: (\d+) tests', content)
        total_match = re.search(r'📈 TOTAL: (\d+) tests', content)
        
        passed = int(passed_match.group(1)) if passed_match else 0
        failed = int(failed_match.group(1)) if failed_match else 0
        errors = int(error_match.group(1)) if error_match else 0
        api_total = int(total_match.group(1)) if total_match else 0
        
        total_passed += passed
        total_failed += failed
        total_errors += errors
        total_tests += api_total
        
        # Determine status
        if failed == 0 and errors == 0:
            status = "✅ ALL TESTS PASSED"
        elif passed > 0:
            status = "⚠️  PARTIAL SUCCESS"
        else:
            status = "❌ ALL TESTS FAILED"
        
        api_summaries.append({
            'name': api_name.upper(),
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'total': api_total,
            'status': status
        })
    
    # Add overall summary
    report += f"""
📊 OVERALL SUMMARY
{'='*40}
✅ Total Passed: {total_passed} tests
❌ Total Failed: {total_failed} tests
⚠️  Total Errors: {total_errors} tests
📈 Total Tests: {total_tests} tests

Success Rate: {(total_passed / total_tests * 100):.1f}% ({total_passed}/{total_tests})

"""
    
    # Add API-specific summaries
    report += f"""
📋 API-SPECIFIC RESULTS
{'='*40}
"""
    
    for api in api_summaries:
        report += f"""
{api['name']} API
{'-' * 20}
Status: {api['status']}
Passed: {api['passed']} | Failed: {api['failed']} | Errors: {api['errors']} | Total: {api['total']}
"""
    
    # Add recommendations
    report += f"""
💡 RECOMMENDATIONS
{'='*40}
"""
    
    if total_failed > 0:
        report += f"""
• {total_failed} tests failed - Review API responses and expected status codes
• Check if API endpoints are working correctly
• Verify authentication tokens and parameters
"""
    
    if total_errors > 0:
        report += f"""
• {total_errors} tests had errors - Check API availability and network connectivity
• Verify API endpoints are accessible
"""
    
    if total_passed == total_tests:
        report += """
• 🎉 All tests passed! Your APIs are working correctly.
"""
    
    report += f"""
• Use curl commands in curl_commands_*.txt files for manual testing
• Check individual result files in results/ directory for detailed information
• Review technical details section for debugging information
"""
    
    # Save summary report
    summary_file = "API_TEST_SUMMARY.txt"
    with open(summary_file, "w") as f:
        f.write(report)
    
    print(f"Summary report generated: {summary_file}")
    print("\n" + "="*50)
    print("QUICK SUMMARY")
    print("="*50)
    print(f"APIs Tested: {len(result_files)}")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed} ({(total_passed/total_tests*100):.1f}%)")
    print(f"Failed: {total_failed}")
    print(f"Errors: {total_errors}")
    print("="*50)

if __name__ == "__main__":
    generate_summary_report()

