""" Service Models """

from datetime import date as Date
from typing import Optional

from pydantic import BaseModel


class BookCard(BaseModel):
    """Book model"""

    title: str
    author: str
    cover_image: str
    read_state: bool
    review: Optional[str] = None


class RepositoryCard(BaseModel):
    """Repository model"""

    name: str
    readme: str
    tldr: str
    languages: str
    commits: int
    html_url: str
    update_time: Date


class JobCard(BaseModel):
    """Job model"""

    job_title: str
    company: str
    start_date: str
    end_date: str


class SkillCard(BaseModel):
    """Skill model"""

    skill: str
    timestamp: str


class EducationCard(BaseModel):
    """Education model"""

    school: str
    degree: str
    start_date: str
    end_date: str
