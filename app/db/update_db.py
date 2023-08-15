""" Commands to update db via cronjob """

from app.db.handler import (
    set_updated,
    update_table,
)
from app.db.models import ApiName, Books, Education, Jobs, Repositories
from app.services.github import get_repository_data
from app.services.goodreads import fetch_books
from app.services.linkedin import user_profile


def update_repositories():
    """Function to update repositories"""
    update_table(get_repository_data(), Repositories)
    set_updated(ApiName.REPOSITORIES)


def update_books():
    """Function to update books"""
    update_table(fetch_books(), Books)
    set_updated(ApiName.BOOKS)


def update_linkedin():
    """Update linkedin profile"""
    linkedin_profile = user_profile()
    update_table(linkedin_profile["jobs"], Jobs)
    set_updated(ApiName.JOBS)
    update_table(linkedin_profile["education"], Education)
    set_updated(ApiName.EDUCATION)


def update_database():
    """Function to update database"""
    try:
        update_repositories()
    except Exception as e:
        print(e)
    try:
        update_books()
    except Exception as e:
        print(e)
    try:
        update_linkedin()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    """ """
    update_database()
