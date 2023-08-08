""" Fetch LinkedIn profile data """

import json
from typing import Dict, List

from linkedin_api import Linkedin

from app.config.settings import Settings
from app.services.models import EducationCard, JobCard

settings = Settings()
LINKEDIN_PROFILE = settings.linkedin_profile

linkedin_api = Linkedin(settings.linkedin_user, settings.linkedin_pass)


def user_profile() -> Dict[str, List[str]]:
    """Fetch user profile"""
    profile = linkedin_api.get_profile(LINKEDIN_PROFILE)
    education = [create_education_card(school) for school in profile["education"]]
    jobs = [create_job_card(job) for job in profile["experience"]]
    return {
        "education": education,
        "jobs": jobs,
    }


def create_education_card(school_data: dict) -> EducationCard:
    """Create education card"""
    time_period_start = school_data["timePeriod"]["startDate"]
    time_period_end = school_data["timePeriod"].get("endDate")
    start_date = f'{time_period_start["year"]}-{time_period_start["month"]}'
    if time_period_end:
        end_date = f'{time_period_end["year"]}-{time_period_end["month"]}'
    else:
        end_date = "Present"
    return EducationCard(
        school=school_data["schoolName"],
        degree=school_data["degreeName"],
        field=school_data["fieldOfStudy"],
        end_date=end_date,
        start_date=start_date,
    )


def create_job_card(job_data: dict) -> JobCard:
    """Create job card"""
    time_period_start = job_data["timePeriod"]["startDate"]
    time_period_end = job_data["timePeriod"].get("endDate")
    start_date = f'{time_period_start["year"]}-{time_period_start["month"]}'
    if time_period_end:
        end_date = f'{time_period_end["year"]}-{time_period_end["month"]}'
    else:
        end_date = "Present"
    return JobCard(
        title=job_data["title"],
        company=job_data["companyName"],
        company_logo=job_data["companyLogoUrl"],
        start_date=start_date,
        end_date=end_date,
        description=job_data["description"],
        location=job_data.get("locationName", "remote"),
        industries=json.dumps(job_data["company"]["industries"]),
    )


def modeled_jobs(list_of_jobs) -> List[JobCard]:
    """Model jobs"""
    return [JobCard.from_orm(job) for job in list_of_jobs]


def modeled_education(list_of_education) -> List[EducationCard]:
    """Model education"""
    return [EducationCard.from_orm(school) for school in list_of_education]
