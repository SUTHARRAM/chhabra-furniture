import os

# Define the folder and file structure
project_structure = {
    "config.py": """# Configuration file
GITHUB_TOKEN = "your_github_token"
OPENAI_API_KEY = "your_openai_api_key"
REPO_OWNER = "repo_owner"
REPO_NAME = "repo_name"
""",
    "requirements.txt": """# Dependencies
requests
openai
pylint
""",
    "main.py": """# Main entry point
from github_api.fetch import fetch_pull_requests, fetch_file_content
from github_api.post import post_comment
from analysis.static_analysis import run_pylint
from analysis.ai_suggestions import suggest_code_improvements

def review_pull_requests():
    pull_requests = fetch_pull_requests()
    for pr in pull_requests:
        pr_number = pr['number']
        files_url = pr['_links']['self']['href'] + "/files"
        files = fetch_pull_requests()  # Fetch files in the PR
        for file in files:
            code = fetch_file_content(file['raw_url'])
            print(f"Analyzing file: {file['filename']}")
            
            # Static analysis
            pylint_output = run_pylint(file['filename'])
            print(f"Pylint Output: {pylint_output}")
            
            # AI suggestions
            suggestions = suggest_code_improvements(code)
            print(f"Suggestions: {suggestions}")
            
            # Post comments
            post_comment(pr_number, f"Suggestions for {file['filename']}:\\n{suggestions}")

if __name__ == "__main__":
    review_pull_requests()
""",
    "github_api/__init__.py": "",
    "github_api/fetch.py": """# GitHub API fetch module
import requests
from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME

def fetch_pull_requests():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching pull requests: {response.status_code}, {response.text}")

def fetch_file_content(file_url):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(file_url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error fetching file content: {response.status_code}, {response.text}")
""",
    "github_api/post.py": """# GitHub API post module
import requests
from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME

def post_comment(pr_number, comment_body):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"body": comment_body}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Comment posted successfully!")
    else:
        raise Exception(f"Error posting comment: {response.status_code}, {response.text}")
""",
    "analysis/__init__.py": "",
    "analysis/static_analysis.py": """# Static analysis module
import subprocess

def run_pylint(file_path):
    result = subprocess.run(["pylint", file_path], capture_output=True, text=True)
    return result.stdout
""",
    "analysis/ai_suggestions.py": """# AI suggestions module
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def suggest_code_improvements(code_snippet):
    prompt = f"Review the following code and suggest improvements:\\n\\n{code_snippet}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
"""
}

# Create folders and files
def create_project_structure(base_path, structure):
    for path, content in structure.items():
        full_path = os.path.join(base_path, path)
        folder = os.path.dirname(full_path)
        os.makedirs(folder, exist_ok=True)  # Create folders if they don't exist
        with open(full_path, "w") as file:
            file.write(content)  # Write content to the file
        print(f"Created: {full_path}")

# Run the setup
if __name__ == "__main__":
    base_path = os.getcwd()  # Current working directory
    create_project_structure(base_path, project_structure)
    print("Project setup complete!")