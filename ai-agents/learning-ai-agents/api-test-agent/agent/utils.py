import yaml
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://merp.intermesh.net")

def load_swagger(api_name: str) -> dict:
    """Load Swagger YAML spec for a given API."""
    file_path = Path("swagger") / f"{api_name}.yaml"
    if not file_path.exists():
        raise FileNotFoundError(f"Swagger file not found: {file_path}")
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def ensure_dirs(api_name: str):
    """Ensure test and results directories exist for API."""
    Path(f"tests/{api_name}").mkdir(parents=True, exist_ok=True)
    Path("results").mkdir(parents=True, exist_ok=True)

def get_paths(api_name: str):
    return {
        "test_file": f"tests/{api_name}/test_{api_name}.py",
        "result_file": f"results/{api_name}.txt"
    }
