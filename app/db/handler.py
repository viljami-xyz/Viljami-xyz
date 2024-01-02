""" Database settings and connection. """

import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import Settings
from app.db.models import (
    ApiName,
    Base,
    Books,
    Education,
    Jobs,
    Repositories,
    Skills,
    UpdateStatus,
)

settings = Settings()

async_engine = create_async_engine(settings.async_db)
engine = create_engine(settings.sync_db)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
session_maker = sessionmaker(engine, expire_on_commit=False)

UPDATE_INTERVAL = datetime.timedelta(hours=1)


def create_db_and_tables():
    """Create database and tables"""
    Base.metadata.create_all(engine)


def set_updated(api_name: ApiName) -> None:
    """Set last updated time for a given api"""
    utcnow = datetime.datetime.utcnow()

    with session_maker() as session:
        stmt = select(UpdateStatus).where(UpdateStatus.api_name == api_name)

        result = session.execute(stmt)
        update = result.scalars().first()
        if not update:
            update = UpdateStatus(api_name=api_name, last_updated=utcnow)
            session.add(update)
        else:
            update.last_updated = utcnow
        session.commit()


def requires_update(api_name: ApiName) -> bool:
    """Get last updated time for a given api"""
    utcnow = datetime.datetime.utcnow()
    with session_maker() as session:
        stmt = select(UpdateStatus).where(UpdateStatus.api_name == api_name)

        result = session.execute(stmt)
        update = result.scalars().first()
        if not update:
            return True
        update_status = UPDATE_INTERVAL < utcnow - update.last_updated
    return update_status


def update_table(api_data: List[BaseModel], table: Base):
    """Update jobs"""
    with session_maker() as session:
        existing_records = get_table_content(table, session)
        for api_item in api_data:
            # Create a new record if no existing record is found
            new_record = table(**api_item.__dict__)
            # Initialize other columns
            if new_record not in existing_records:
                session.add(new_record)
        # Commit the changes
        session.commit()


def get_table_content(table: Base, session: Session):
    """Get table contents"""
    stmt = select(table)
    result = session.execute(stmt)
    if not result:
        return None
    table_content = result.scalars().all()

    return table_content


def get_repositories():
    """Get repositories"""
    with session_maker() as session:
        stmt = select(Repositories)
        result = session.execute(stmt)
        if not result:
            return None
        repos = result.scalars().all()

    return repos


### Async functions
async def async_get_jobs():
    """Get jobs"""
    async with async_session_maker() as session:
        stmt = select(Jobs)
        result = await session.execute(stmt)
        if not result:
            return None
        jobs = result.scalars().all()

    return jobs


async def async_get_skills():
    """Get skills"""
    async with async_session_maker() as session:
        stmt = select(Skills)
        result = await session.execute(stmt)
        if not result:
            return None
        skills = result.scalars().all()

    return skills


async def async_get_books():
    """Get books"""
    async with async_session_maker() as session:
        stmt = select(Books)
        result = await session.execute(stmt)
        if not result:
            return None
        books = result.scalars().all()

    return books


async def async_get_repositories():
    """Get repositories"""
    async with async_session_maker() as session:
        stmt = select(Repositories)
        result = await session.execute(stmt)
        if not result:
            return None
        repos = result.scalars().all()

    return repos


async def async_get_education():
    """Get education"""
    async with async_session_maker() as session:
        stmt = select(Education)
        result = await session.execute(stmt)
        if not result:
            return None
        education = result.scalars().all()

    return education
