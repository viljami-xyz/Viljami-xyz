""" Commands to update db via cronjob """

from app.db.handler import (
    set_updated,
    update_table,
)
from app.db.models import ApiName, Books, Education, Jobs, Repositories
from app.services.github import get_repository_data
from app.services.goodreads import fetch_books
from app.services.linkedin import user_profile


def update_database():
    """Function to update database"""
    update_table(get_repository_data(), Repositories)
    update_table(fetch_books(), Books)
    linkedin_profile = user_profile()
    update_table(linkedin_profile["jobs"], Jobs)
    update_table(linkedin_profile["education"], Education)
    # Mark all tables as updated
    set_updated(ApiName.REPOSITORIES)
    set_updated(ApiName.BOOKS)
    set_updated(ApiName.JOBS)
    set_updated(ApiName.EDUCATION)


if __name__ == "__main__":
    """ """
    update_database()
