""" Service Models """

import json
from datetime import date as Date
from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta


class BookCard(BaseModel):
    """Book model"""

    title: str
    author: str
    cover_image: str
    read_state: bool
    date_added: str
    review: Optional[str] = None

    class Config:
        """Configure ORM mode"""

        orm_mode = True


class RepositoryCard(BaseModel):
    """Repository model"""

    name: str
    readme: str
    tldr: str
    languages: str | dict
    commits: int
    html_url: str
    update_time: Date

    class Config:
        """Configure ORM mode"""

        orm_mode = True


def repo_from_orm(sql_instance: DeclarativeMeta) -> RepositoryCard:
    """Convert ORM object to Pydantic object"""
    repo = RepositoryCard.from_orm(sql_instance)
    repo.languages = json.loads(repo.languages)
    return repo


class JobCard(BaseModel):
    """Job model"""

    job_title: str
    company: str
    start_date: str
    end_date: str

    class Config:
        """Configure ORM mode"""

        orm_mode = True


class SkillCard(BaseModel):
    """Skill model"""

    skill: str
    timestamp: str

    class Config:
        """Configure ORM mode"""

        orm_mode = True


class EducationCard(BaseModel):
    """Education model"""

    school: str
    degree: str
    start_date: str
    end_date: str

    class Config:
        """Configure ORM mode"""

        orm_mode = True
