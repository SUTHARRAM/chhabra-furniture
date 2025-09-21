from github_api.fetch import fetch_pull_requests, fetch_file_content
from github_api.post import post_comment
from analysis.static_analysis import run_pylint
from analysis.ai_suggestions import suggest_code_improvements
import requests
from config import GITHUB_TOKEN

def fetch_pull_request_files(files_url):
    """Fetch files for a specific pull request."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(files_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching pull request files: {response.status_code}, {response.text}")

def review_pull_requests():
    pull_requests = fetch_pull_requests()
    for pr in pull_requests:
        pr_number = pr['number']
        files_url = pr['_links']['self']['href'] + "/files"
        
        # Fetch files for the pull request
        files = fetch_pull_request_files(files_url)
        print(f"Files Response: {files}")  # Debugging: Print the files response
        
        for file in files:
            # Use the correct key for the file URL
            file_url = file.get('raw_url') or file.get('contents_url') or file.get('download_url')
            if not file_url:
                print(f"Skipping file: {file['filename']} (no valid URL found)")
                continue
            
            code = fetch_file_content(file_url)
            print(f"Analyzing file: {file['filename']}")
            
            # Static analysis
            pylint_output = run_pylint(file['filename'])
            print(f"Pylint Output: {pylint_output}")
            
            # AI suggestions
            suggestions = suggest_code_improvements(code)
            print(f"Suggestions: {suggestions}")
            
            # Post comments
            post_comment(pr_number, f"Suggestions for {file['filename']}:\n{suggestions}")

if __name__ == "__main__":
    review_pull_requests()