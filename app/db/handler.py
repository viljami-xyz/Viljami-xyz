""" Database settings and connection. """

import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

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

engine = create_async_engine(settings.testdb)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

UPDATE_INTERVAL = datetime.timedelta(hours=1)


async def create_db_and_tables():
    """Create database and tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def requires_update(api_name: ApiName) -> bool:
    """Get last updated time for a given api"""
    utcnow = datetime.datetime.utcnow()
    async with async_session_maker() as session:
        stmt = select(UpdateStatus).where(UpdateStatus.api_name == api_name)

        result = await session.execute(stmt)
        update = result.scalars().first()
        if not update:
            return True
        update_status = UPDATE_INTERVAL < utcnow - update.last_updated
    return update_status


async def set_updated(api_name: ApiName) -> None:
    """Set last updated time for a given api"""
    utcnow = datetime.datetime.utcnow()
    async with async_session_maker() as session:
        stmt = select(UpdateStatus).where(UpdateStatus.api_name == api_name)

        result = await session.execute(stmt)
        update = result.scalars().first()
        if not update:
            update = UpdateStatus(api_name=api_name, last_updated=utcnow)
            session.add(update)
        else:
            update.last_updated = utcnow
        await session.commit()


async def get_jobs():
    """Get jobs"""
    async with async_session_maker() as session:
        stmt = select(Jobs)
        result = await session.execute(stmt)
        if not result:
            return None
        jobs = result.scalars().all()

    return jobs


async def get_skills():
    """Get skills"""
    async with async_session_maker() as session:
        stmt = select(Skills)
        result = await session.execute(stmt)
        if not result:
            return None
        skills = result.scalars().all()

    return skills


async def get_books():
    """Get books"""
    async with async_session_maker() as session:
        stmt = select(Books)
        result = await session.execute(stmt)
        if not result:
            return None
        books = result.scalars().all()

    return books


async def get_repositories():
    """Get repositories"""
    async with async_session_maker() as session:
        stmt = select(Repositories)
        result = await session.execute(stmt)
        if not result:
            return None
        repos = result.scalars().all()

    return repos


async def get_education():
    """Get education"""
    async with async_session_maker() as session:
        stmt = select(Education)
        result = await session.execute(stmt)
        if not result:
            return None
        education = result.scalars().all()

    return education


async def update_table(api_data: List[BaseModel], table: Base):
    """Update jobs"""
    async with async_session_maker() as session:
        existing_records = await get_repositories()
        for api_item in api_data:
            # Create a new record if no existing record is found
            new_record = table(**api_item.__dict__)
            # Initialize other columns
            session.add(new_record)
        if existing_records:
            session.delete(existing_records)
        # Commit the changes
        await session.commit()
