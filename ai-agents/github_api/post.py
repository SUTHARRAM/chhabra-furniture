# GitHub API post module
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
