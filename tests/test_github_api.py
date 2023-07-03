""" Test the GitHub API """


from typing import List, Dict

import pytest

from app.services.github import GithubRepos

REPONAME = "hintascraper"


@pytest.fixture
def github_client():
    """Test GithubRepos creation"""
    return GithubRepos()


def test_get_repository(github_client):
    """Test repository property"""

    repository_data = github_client.get_repository_data({"name": REPONAME})

    assert repository_data["name"] == REPONAME


def test_get_commits(github_client):
    """Test commits"""
    repo_commits = github_client.get_commits(REPONAME)
    assert isinstance(
        repo_commits,
        int,
    )


def test_readme(github_client):
    """Test readme"""
    repo_readme = github_client.get_readme(REPONAME)
    assert isinstance(repo_readme, str)


def test_languages(github_client):
    """Test languages"""
    repo_languages = github_client.get_languages(REPONAME)
    assert isinstance(
        repo_languages,
        dict,
    )


def test_update_time(github_client):
    """Test update time"""
    repo_update_time = github_client.get_update_time(REPONAME)
    assert isinstance(
        repo_update_time,
        str,
    )
