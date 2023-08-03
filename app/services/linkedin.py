""" Fetch LinkedIn profile data """

import os

from dotenv import load_dotenv
from linkedin_api import Linkedin

load_dotenv("app/config/.env")

USER = os.getenv("LINKEDIN_USER")
PASS = os.getenv("LINKEDIN_PASS")


class LinkedInProfile:
    """Fetch LinkedIn profile data for web page"""

    def __init__(self):
        self.api = Linkedin(USER, PASS)

    def user_profile(self):
        """Fetch user profile"""
        return self.api.get_profile("viljami-kilkkila")
