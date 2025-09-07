# GitHub API fetch module
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
