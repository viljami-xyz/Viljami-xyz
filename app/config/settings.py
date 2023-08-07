""" Config file for the app"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings class for the app"""

    app_name: str = "FastAPI"
    github_api_key: str

    testuser: str
    testpass: str
    sync_db: str
    async_db: str

    linkedin_user: str
    linkedin_pass: str
    linkedin_profile: str

    class Config:
        """
        Configuration for environment settings

        Parameters
        ----------
        Config : Config
            Configuration for environment settings
        """

        env_file = "app/config/.env"
        env_file_encoding = "utf-8"
        case_sensitive = False
