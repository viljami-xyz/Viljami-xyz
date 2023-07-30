""" Config file for the app"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings class for the app"""

    app_name: str = "FastAPI"
    github_api_key: str

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