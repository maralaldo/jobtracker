import asyncio
import logging
from typing import List, Dict
from app.core.celery import celery_app
from app.core.database import AsyncSessionLocal
from app.models.vacancy import Vacancy
from sqlalchemy import select


logger = logging.getLogger(__name__)


async def save_vacancies_to_db(vacancies: List[Dict]) -> int:
    added = 0
    async with AsyncSessionLocal() as session:
        for v in vacancies:
            stmt = select(Vacancy).where(Vacancy.url == v["url"])
            res = await session.execute(stmt)
            existing = res.scalar_one_or_none()
            if existing:
                continue

            db_v = Vacancy(
                title=v["title"],
                company=v["company"],
                location=v.get("location"),
                salary=v.get("salary"),
                url=v["url"],
                source=v.get("source"),
            )
            session.add(db_v)
            added += 1

        if added:
            await session.commit()
        else:
            await session.commit()
    return added


@celery_app.task(name="app.tasks.vacancies.parse_vacancies")
def parse_vacancies():
    logger.info("Starting parse_vacancies (mock)")

# TODO: Replace the mock with a real parser (requests/aiohttp)
    mock_vacancies = [
        {
            "title": "Python Developer",
            "company": "OpenAI",
            "location": "Remote",
            "salary": 150000,
            "url": "https://example.com/jobs/python-1",
            "source": "mock",
        },
        {
            "title": "Backend Engineer",
            "company": "Acme",
            "location": "Minsk",
            "salary": 80000,
            "url": "https://example.com/jobs/backend-1",
            "source": "mock",
        },
    ]

    added = asyncio.run(save_vacancies_to_db(mock_vacancies))

    logger.info("parse_vacancies finished: added=%d", added)
    return {"added": added, "total_found": len(mock_vacancies)}
