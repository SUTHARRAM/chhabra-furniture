# Static analysis module
import subprocess

def run_pylint(file_path):
    result = subprocess.run(["pylint", file_path], capture_output=True, text=True)
    return result.stdout
