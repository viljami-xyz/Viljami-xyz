""" Database models """


import datetime
from enum import Enum, auto

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    String,
)
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import DeclarativeBase


class ApiName(str, Enum):
    """API names"""

    JOBS = auto()
    SKILLS = auto()
    EDUCATION = auto()
    REPOSITORIES = auto()
    BOOKS = auto()


class Base(DeclarativeBase):
    """Base class for ORM models"""


class UpdateStatus(Base):
    """Check the last time the database was updated"""

    __tablename__ = "update_status"

    api_name = Column(SQLAlchemyEnum(ApiName), primary_key=True)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class Repositories(Base):
    """Reflection model"""

    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    readme = Column(String, nullable=False)
    tldr = Column(String, nullable=False)
    languages = Column(String, nullable=False)
    commits = Column(String, nullable=False)
    html_url = Column(String, nullable=False)
    update_time = Column(Date, nullable=False)


class Books(Base):
    """Qeustion model"""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    cover_image = Column(String, nullable=False)
    read_state = Column(Boolean, default=False)
    review = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    date_added = Column(String, nullable=False)


class Jobs(Base):
    """Qeustion model"""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)


class Skills(Base):
    """Qeustion model"""

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill = Column(String, nullable=False)
    timestamp = Column(Date, nullable=False)


class Education(Base):
    """Qeustion model"""

    __tablename__ = "education"

    id = Column(Integer, primary_key=True, autoincrement=True)
    school = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
