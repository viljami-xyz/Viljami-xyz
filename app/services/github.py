""" Test the GitHub API """

import base64
import json
import pathlib
from datetime import datetime
from typing import Any, Dict, List

import requests

from app.config.settings import Settings
from app.services.models import RepositoryCard

settings = Settings()

saved_repos = pathlib.Path("app/static/repositories.json")


owner = "viljami-xyz"
access_token = settings.github_api_key

base_url = f"https://api.github.com/repos/{owner}"


def _make_request(
    method, endpoint, params=None, data=None, custom_url=None
) -> List[dict]:
    """Custom request with token"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    if custom_url:
        url = custom_url + endpoint
    else:
        url = base_url + endpoint

    response = requests.request(
        method, url, headers=headers, params=params, json=data, timeout=5
    )

    return response.json()


def get_repository_data() -> List[RepositoryCard]:
    """Fetch repositories from GitHub"""

    list_of_repos = []
    url = f"https://api.github.com/users/{owner}/repos"
    repos_response = _make_request(method="GET", endpoint="", custom_url=url)
    for repo in repos_response:
        repo = {
            key: value for key, value in repo.items() if key in ["name", "html_url"]
        }
        repo = create_repo_card(repo)
        repo_card = RepositoryCard(**repo)
        list_of_repos.append(repo_card)

    return list_of_repos


def create_repo_card(repo: dict) -> Dict[str, Any]:
    """Get repository data for single repo"""

    repo["commits"] = get_commits(repo["name"])
    repo["update_time"] = get_update_time(repo["name"])
    repo["languages"] = get_languages(repo["name"])
    repo["readme"] = get_readme(repo["name"])
    repo["tldr"] = get_readme_tldr(repo["readme"])
    return repo


def get_commits(repo) -> int:
    """Fetch commits"""
    commits_url = f"/{repo}/commits"
    commits = _make_request("GET", commits_url)
    return len(commits)


def get_update_time(repo) -> str:
    """Fetch repository update details"""
    repo_url = f"/{repo}"
    repo_details = _make_request("GET", repo_url)
    updated_at = repo_details.get("updated_at", None).split("T")[0]
    updated_at = datetime.strptime(updated_at, "%Y-%m-%d").date()

    return updated_at


def get_languages(repo) -> Dict[str, float]:
    """Fetch languages"""
    languages_url = f"/{repo}/languages"
    languages = _make_request("GET", languages_url)
    total = sum(languages.values())
    languages = {k: round(v / total * 100, 2) for k, v in languages.items()}
    return json.dumps(languages)


def get_readme(repo) -> str:
    """Fetch README"""
    readme_url = f"/{repo}/readme"
    readme_data = _make_request("GET", readme_url)

    # Extract the base64-encoded content from the response
    try:
        readme_content = base64.b64decode(readme_data["content"]).decode("utf-8")
    except KeyError:
        readme_content = "No README available"

    return readme_content


def get_readme_tldr(readme) -> str:
    """If the README is longer than 25 characters,
    return the first 25 characters"""
    if len(readme) > 25:
        return readme[:22] + "..."
    return readme
