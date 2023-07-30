""" Test the GitHub API """

import base64
import json
import pathlib
import time
from typing import Any, Dict, List

import requests

from app.config.settings import Settings

settings = Settings()

saved_repos = pathlib.Path("app/static/repositories.json")


class GithubRepos:
    """Fetch repositories from GitHub"""

    owner = "viljami-xyz"
    access_token = settings.github_api_key
    timestamp = time.time()

    def __init__(self):
        self.base_url = f"https://api.github.com/repos/{self.owner}"

    def _make_request(
        self, method, endpoint, params=None, data=None, custom_url=None
    ) -> List[dict]:
        """Custom request with token"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        if custom_url:
            url = custom_url + endpoint
        else:
            url = self.base_url + endpoint

        response = requests.request(
            method, url, headers=headers, params=params, json=data, timeout=5
        )

        return response.json()

    @property
    def repository_data(self) -> List[dict]:
        """Fetch repositories from GitHub"""
        if not self.fetch_interval and saved_repos.exists():
            return self.load_repositories

        list_of_repos = []
        url = f"https://api.github.com/users/{self.owner}/repos"
        repos_response = self._make_request(method="GET", endpoint="", custom_url=url)
        for repo in repos_response:
            repo = {
                key: value for key, value in repo.items() if key in ["name", "html_url"]
            }
            repo = self.get_repository_data(repo)
            list_of_repos.append(repo)
        self.save_repositories(list_of_repos)
        return list_of_repos

    @property
    def fetch_interval(self) -> bool:
        """Check the difference between timestamp and current time,
        if more than 1 hour, return True"""
        return time.time() - self.timestamp > 3600

    def get_repository_data(self, repo: dict) -> Dict[str, Any]:
        """Get repository data for single repo"""
        repo["commits"] = self.get_commits(repo["name"])
        repo["update_time"] = self.get_update_time(repo["name"])
        repo["languages"] = self.get_languages(repo["name"])
        repo["readme"] = self.get_readme(repo["name"])
        repo["tldr"] = self.get_readme_tldr(repo["readme"])
        return repo

    def get_commits(self, repo) -> int:
        """Fetch commits"""
        commits_url = f"/{repo}/commits"
        commits = self._make_request("GET", commits_url)
        return len(commits)

    def get_update_time(self, repo) -> str:
        """Fetch repository update details"""
        repo_url = f"/{repo}"
        repo_details = self._make_request("GET", repo_url)
        updated_at = repo_details.get("updated_at", None).split("T")[0]
        return updated_at

    def get_languages(self, repo) -> Dict[str, float]:
        """Fetch languages"""
        languages_url = f"/{repo}/languages"
        languages = self._make_request("GET", languages_url)
        total = sum(languages.values())
        languages = {k: round(v / total * 100, 2) for k, v in languages.items()}
        return languages

    def get_readme(self, repo) -> str:
        """Fetch README"""
        readme_url = f"/{repo}/readme"
        readme_data = self._make_request("GET", readme_url)

        # Extract the base64-encoded content from the response
        try:
            readme_content = base64.b64decode(readme_data["content"]).decode("utf-8")
        except KeyError:
            readme_content = "No README available"

        return readme_content

    def get_readme_tldr(self, readme) -> str:
        """If the README is longer than 25 characters,
        return the first 25 characters"""
        if len(readme) > 25:
            return readme[:22] + "..."
        return readme

    def save_repositories(self, list_of_repos: List[dict]):
        """Save repositories to file"""
        with open(saved_repos, "w", encoding="UTF-8") as file:
            json.dump(list_of_repos, file)

    @property
    def load_repositories(self) -> List[dict]:
        """Load repositories from file"""
        with open(saved_repos, "r", encoding="UTF-8") as file:
            list_of_repos = json.load(file)
        return list_of_repos
